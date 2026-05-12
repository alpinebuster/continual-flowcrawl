import asyncio
import os
import uuid
from datetime import datetime
import signal
import sys
import re
import time
import random
import subprocess
from urllib.parse import urlparse
from multiprocessing import cpu_count
from pathlib import Path

DOCKER_IMAGE = "sitespeedio/browsertime:latest"

TIMEOUT = 600 # Maximum time for each task (in seconds)
RETRY = 2       # Number of retries

SAMPLES_PER_SITE = 100

WORKERS = min(6, cpu_count())
print(f"Workers: {WORKERS}")
NETWORKS = [f"flowcrawl-net-{i}" for i in range(WORKERS)]


def extract_urls(file_path: Path) -> list[str]:
    urls = set()
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            matches = re.findall(r"https://[^\s]+", line)
            urls.update(matches)
    return list(urls)


def collect_txt_files(input_path: str) -> list[Path]:
    p = Path(input_path)
    if p.is_file():
        return [p]
    elif p.is_dir():
        return list(p.rglob("*.txt"))
    return []


def is_task_done(output_dir: str, samples_per_site: int = 100) -> bool:
    p = Path(output_dir)

    valid = 0
    for d in p.iterdir():
        if not d.is_dir():
            continue

        if (d / "browsertime.json").exists():
            valid += 1

    return valid >= samples_per_site


def ensure_networks(networks: list):
    for net in networks:
        result = subprocess.run(
            ["docker", "network", "inspect", net],
        )
        if result.returncode != 0:
            print(f"[+] Creating network: {net}")
            subprocess.run(["docker", "network", "create", net], check=True)

            result_again = subprocess.run(
                ["docker", "network", "inspect", net],
            )
            if result_again.returncode != 0:
                raise Exception(f"[!] Can NOT create the network: {net}")


async def run_cmd(cmd, timeout):
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        # IMPORTANT:
        # create separate process group
        preexec_fn=os.setsid,
    )

    try:
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(),
            timeout=timeout,
        )
    except asyncio.TimeoutError:
        print("[run_cmd] timeout reached")
        # Graceful terminate process group
        try:
            os.killpg(proc.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass

        # Give it a chance to exit cleanly
        try:
            await asyncio.wait_for(proc.wait(), timeout=12)
        except asyncio.TimeoutError:
            # Force kill if still alive
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass

        raise asyncio.TimeoutError()

    # Print subprocess output
    if stdout:
        print(stdout.decode(errors="ignore"), flush=True)
    if stderr:
        print(stderr.decode(errors="ignore"), flush=True)

    assert proc.returncode is not None
    if proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, cmd)


def cleanup_container(container_name):
    """
    Force cleanup docker container safely.
    """
    # Graceful stop first
    subprocess.run(
        [
            "docker",
            "stop",
            "-t",
            "12",
            container_name,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    # Force remove
    subprocess.run(
        [
            "docker",
            "rm",
            "-f",
            container_name,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def cleanup_tcpdump():
    """
    [!] Emergency cleanup for leaked tcpdump.
    """
    subprocess.run(
        ["pkill", "-f", "tcpdump"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


async def worker(worker_id, network, queue):
    while True:
        task = await queue.get()
        if task is None:
            queue.task_done()
            break

        url, output_dir, idx = task
        # Startup jitter
        await asyncio.sleep(random.uniform(1.2, 3.6))

        container_name = f"bt-w_{worker_id}-i_{idx}-{int(time.time())}"
        nopasswd_config_path = os.path.join(os.getcwd(), "config/browsertime-sudoers/nopasswd")
        cmd = [
            "docker", "run",
            "--rm",
            "--network", network,
            "--name", container_name,
            "-v", f"{output_dir}:{output_dir}",
            # NOTE: this fixes `sudo: a terminal is required to read the password;`
            "-v", f"{nopasswd_config_path}:/etc/sudoers.d/nopasswd:ro",
            DOCKER_IMAGE,

            "-n", "1",
            "--resultDir", f"{output_dir}",
            "--video", "--tcpdump", "--visualMetrics",
            # Wait up to 10 seconds for elements
            # "--timeouts.elementWait", "10000",

            "--browser", "chrome",
            "--chrome.args", "enable-features=EncryptedClientHello",
            "--chrome.args", "use-dns-https-alpn",
            "--chrome.args", "force-dns-over-https=https://cloudflare-dns.com/dns-query",
            "--chrome.args", "disable-async-dns",
            "--chrome.collectNetLog",
            "--chrome.args", "disable-background-networking",
            "--chrome.args", "disable-component-update",
            "--chrome.args", "disable-sync",
            "--chrome.args", "disable-default-apps",
            "--chrome.args", "disable-domain-reliability",
            "--chrome.args", "disable-extensions",

            # "--chrome.args", "user-data-dir=/tmp/chrome-profile-bt",
            url,
        ]

        success = False
        for attempt in range(RETRY):
            try:
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                print(
                    f"[{now}] "
                    f"[W{worker_id}][{idx}] "
                    f"RUN ({attempt+1}/{RETRY}) {url}"
                )
                await run_cmd(cmd, TIMEOUT)
                print(f"[W{worker_id}][{idx}] SUCCESS {url}")
                success = True
                break
            except asyncio.TimeoutError:
                print(f"[W{worker_id}][{idx}] TIMEOUT {url}")
                cleanup_container(container_name)
                print(f"[W{worker_id}][{idx}] TIMEOUT {url} -> killed {container_name}")
            except Exception as e:
                print(f"[W{worker_id}][{idx}] ERROR {url}: {e}")
                cleanup_container(container_name)
                print(f"[W{worker_id}][{idx}] ERROR {url} -> killed {container_name}")
            await asyncio.sleep(5 * (attempt + 1))

        if not success:
            print(f"[W{worker_id}][{idx}] FAILED {url}")

        queue.task_done()


async def delayed_worker(delay, i, net, queue):
    await asyncio.sleep(delay)
    await worker(i, net, queue)


async def main_async(tasks):
    queue = asyncio.Queue()

    for t in tasks:
        await queue.put(t)

    # Start the worker (each bound to one network)
    workers = []
    for i, net in enumerate(NETWORKS):
        workers.append(
            asyncio.create_task(
                delayed_worker(i*0.2, i, net, queue)
            )
        )

    # Wait until the task is completed
    await queue.join()
    # Stop the worker
    for _ in workers:
        await queue.put(None)
    await asyncio.gather(*workers)


def main():
    print("=== SCRIPT STARTED ===", flush=True)
    if len(sys.argv) < 2:
        print("Usage: `python run_browsertime.py <file_or_dir>`")
        return
    ensure_networks(NETWORKS)

    input_path = sys.argv[1]
    txt_files = collect_txt_files(input_path)

    if not txt_files:
        print("No txt files found.")
        return

    all_urls = set()
    for txt in txt_files:
        urls = extract_urls(txt)
        all_urls.update(urls)
    print(f"Total raw URLs: {len(all_urls)}")

    tasks = []
    task_id = 0
    for _, url in enumerate(sorted(all_urls)):
        parsed = urlparse(url)
        domain = parsed.netloc

        domain_output_dir = os.path.abspath(f"output/{domain}")
        # Skip completed
        if is_task_done(
            domain_output_dir,
            SAMPLES_PER_SITE,
        ):
            print(f"[SKIP] {url}")
            continue

        # Repeat `SAMPLES_PER_SITE` times for each URL
        for _ in range(SAMPLES_PER_SITE):
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            uid = uuid.uuid4().hex[:8]
            output_dir = os.path.abspath(
                f"{domain_output_dir}/{timestamp}-{uid}"
            )

            if not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)

            print(f"[+] Create task_{task_id} [{url}, output_dir: {output_dir}]")
            tasks.append((url, output_dir, task_id))
            task_id += 1

    print(f"Tasks to run: {len(tasks)}")
    if not tasks:
        print("Nothing to do.")
        return

    asyncio.run(main_async(tasks))


if __name__ == "__main__":
    """
    Example:

    nohup python -u \
      ./flowcrawl/run_browsertime.py \
      data/links-for-request/ech/links-CF.txt \
      > run_browsertime.log 2>&1 &

    ps -aux | grep run_browsertime
    pkill -f run_browsertime
    """
    main()
