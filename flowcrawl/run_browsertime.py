import asyncio
import os
import sys
import re
import time
import random
import subprocess
from urllib.parse import urlparse
from multiprocessing import cpu_count
from pathlib import Path

DOCKER_IMAGE = "sitespeedio/browsertime:latest"

TIMEOUT = 43200 # Maximum time for each task (in seconds, # 12 hours)
RETRY = 2       # Number of retries

SAMPLES_PER_SITE = 100

WORKERS = min(2, cpu_count())
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


def is_task_done(output_dir: str) -> bool:
    for path in Path(output_dir).rglob("browsertime.json"):
        if path.stat().st_size > 1000:
            return True
    return False


def ensure_networks(networks: list):
    for net in networks:
        result = subprocess.run(
            ["docker", "network", "inspect", net],
        )
        if result.returncode != 0:
            print(f"[+] Creating network: {net}")
            subprocess.run(["docker", "network", "create", net], check=True)


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
            await asyncio.wait_for(proc.wait(), timeout=10)
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
            "15",
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
    Emergency cleanup for leaked tcpdump.
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

        os.makedirs(output_dir, exist_ok=True)
        # Startup jitter
        await asyncio.sleep(random.uniform(0.5, 2.0))

        container_name = f"bt-{worker_id}-{idx}-{int(time.time())}"
        cmd = [
            "docker", "run",
            # "--rm",
            "--network", network,
            "--name", container_name,
            "-v", f"{output_dir}:/browsertime",
            DOCKER_IMAGE,

            "-n", str(SAMPLES_PER_SITE),
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
                print(f"[W{worker_id}][{idx}] RUN ({attempt+1}/{RETRY+1}) {url}")
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

        if not success:
            print(f"[W{worker_id}][{idx}] FAILED {url}")

        queue.task_done()


async def main_async(tasks):
    queue = asyncio.Queue()

    for t in tasks:
        await queue.put(t)

    # Start the worker (each bound to one network)
    workers = []
    for i, net in enumerate(NETWORKS):
        workers.append(asyncio.create_task(worker(i, net, queue)))

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
    for i, url in enumerate(sorted(all_urls)):
        parsed = urlparse(url)
        domain = parsed.netloc
        output_dir = os.path.abspath(f"output/{domain}")

        # Skip completed
        if is_task_done(output_dir):
            print(f"[SKIP] {url}")
            continue
        tasks.append((url, output_dir, i))

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
    """
    main()
