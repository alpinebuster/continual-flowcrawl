import os
import sys
import re
import time
import random
import subprocess
from urllib.parse import urlparse
from multiprocessing import Pool, cpu_count, Manager
from pathlib import Path

DOCKER_IMAGE = "sitespeedio/browsertime:26.3.2"

TIMEOUT = 600   # Maximum time for each task (in seconds)
RETRY = 2       # Number of retries

SAMPLES_PER_SITE = 100

WORKERS = min(2, cpu_count())
print(f"Workers: {WORKERS}")
NETWORKS = [f"flowcrawl-net-{i}" for i in range(WORKERS)]

manager = Manager()
NET_QUEUE = manager.Queue()
for net in NETWORKS:
    NET_QUEUE.put(net)

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
    result_file = os.path.join(output_dir, "browsertime.json")
    # ≈ 1 KB
    return os.path.exists(result_file) and os.path.getsize(result_file) > 1000


def ensure_networks(networks: list):
    for net in networks:
        result = subprocess.run(
            ["docker", "network", "inspect", net],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if result.returncode != 0:
            print(f"[+] Creating network: {net}")
            subprocess.run(["docker", "network", "create", net], check=True)


def run_task(args: tuple):
    url, output_dir, idx, network_queue = args

    # Startup jitter
    time.sleep(random.uniform(0.5, 2.0))
    os.makedirs(output_dir, exist_ok=True)
    # Obtain an exclusive network (blocking)
    network = network_queue.get()

    try:
        cmd = [
            "docker", "run", "--rm",
            "--network", network,
            "-v", f"{output_dir}:/browsertime",
            DOCKER_IMAGE,
            "-n", SAMPLES_PER_SITE,
            "--video", "--tcpdump", "--visualMetrics",
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
            url,
        ]

        for attempt in range(RETRY + 1):
            try:
                print(f"[{idx}] RUN ({attempt+1}/{RETRY+1}) {url}")
                subprocess.run(cmd, timeout=TIMEOUT, check=True)
                return f"[{idx}] SUCCESS {url}"

            except subprocess.TimeoutExpired:
                print(f"[{idx}] TIMEOUT {url}")

            except subprocess.CalledProcessError:
                print(f"[{idx}] ERROR {url}")

    finally:
        # It must be returned after use
        network_queue.put(network)

    return f"[{idx}] FAILED {url}"


def main():
    if len(sys.argv) < 2:
        print("Usage: python run_browsertime.py <file_or_dir>")
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
        output_dir = os.path.abspath(f"data/{domain}")

        # Skip completed
        if is_task_done(output_dir):
            print(f"[SKIP] {url}")
            continue
        tasks.append((url, output_dir, i, NET_QUEUE))

    print(f"Tasks to run: {len(tasks)}")
    if not tasks:
        print("Nothing to do.")
        return

    with Pool(WORKERS) as pool:
        results = pool.map(run_task, tasks)

    success = sum(1 for r in results if "SUCCESS" in r)
    failed = sum(1 for r in results if "FAILED" in r)
    print("\n===== SUMMARY =====")
    print(f"Success: {success}")
    print(f"Failed : {failed}")
    print("===================")
    for r in results:
        print(r)


if __name__ == "__main__":
    main()
