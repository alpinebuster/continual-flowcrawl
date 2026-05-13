#!/usr/bin/env python3

import argparse
import subprocess
import signal
from pathlib import Path
import sys
import time
import os


PROCESSES = [] # type:ignore

DEFAULT_LINK_FILE = "data/links-for-request/top-1000-websites.txt"
SOCKS_PROXY = "socks5h://127.0.0.1:27890"

START_WAIT = 5
END_WAIT = 5
CURL_TIMEOUT = 15

def sanitize_dirname(url: str) -> str:
    return (
        url.replace("https://", "")
           .replace("http://", "")
           .replace("/", "_")
           .replace(":", "_")
    )

def run_cmd(cmd: str):
    return subprocess.check_output(cmd, shell=True).decode().strip()

def start_tcpdump(cmd: list[str]):
    print(f"[+] Starting: {' '.join(cmd)}")
    return subprocess.Popen(
        cmd,
        preexec_fn=os.setsid,
    )

def cleanup(signum=None, frame=None):
    print("\n[!] Stopping all tcpdump processes...")

    global PROCESSES

    for p in PROCESSES:
        try:
            os.killpg(os.getpgid(p.pid), signal.SIGTERM)
        except Exception:
            pass

    time.sleep(1)

    for p in PROCESSES:
        try:
            os.killpg(os.getpgid(p.pid), signal.SIGKILL)
        except Exception:
            pass

    print("[+] Clean exit.")
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)


def get_container_ip(name):
    cmd = f"docker inspect -f '{{{{range.NetworkSettings.Networks}}}}{{{{.IPAddress}}}}{{{{end}}}}' {name}"
    return run_cmd(cmd)

def get_bridge_name(network_name):
    # Get network ID → br-xxxx
    net_id = run_cmd(f"docker network inspect -f '{{{{.Id}}}}' {network_name}")
    return f"br-{net_id[:12]}"

def get_subnet(network_name):
    cmd = f"docker network inspect -f '{{{{(index .IPAM.Config 0).Subnet}}}}' {network_name}"
    return run_cmd(cmd)

def run_curl(url: str):
    cmd = [
        "curl",
        # "-L",
        "-sS",
        "--max-time",
        str(CURL_TIMEOUT),
        "-x",
        SOCKS_PROXY,
        url,
    ]

    print(f"[+] Requesting: {url}")
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        print(f"[+] curl return code: {result.returncode}")
        # print("\n===== STDOUT =====")
        # print(result.stdout)
        if result.stderr:
            print("\n===== STDERR =====")
            print(result.stderr)
    except Exception as e:
        print(f"[!] curl failed: {e}")


def main(link_file: str, output_dirname: str):
    """
    curl -x socks5h://127.0.0.1:27890 'https://google.com/'
    tcpdump -r ./data/pcap/stage2_clash.pcap
    """
    print("[*] Fetching container info...")
    CLASH_IP = get_container_ip("clash")
    NETWORK_NAME = "continual-flowcrawl_clashnet"
    BRIDGE = get_bridge_name(NETWORK_NAME)
    SUBNET = get_subnet(NETWORK_NAME)

    print(f"[+] CLASH_IP = {CLASH_IP}")
    print(f"[+] BRIDGE   = {BRIDGE}")
    print(f"[+] SUBNET   = {SUBNET}")

    with open(link_file, "r") as f:
        websites = [
            line.strip()
            for line in f
            if line.strip()
        ]
    print(f"[+] Loaded {len(websites)} websites")
    for idx, site in enumerate(websites):
        if not site.startswith("http://") and not site.startswith("https://"):
            url = f"https://{site}"
        else:
            url = site

        url_dirname = sanitize_dirname(url)
        output_dir = os.path.join(output_dirname, url_dirname)
        os.makedirs(output_dir, exist_ok=True)
        if os.listdir(output_dir):
            print(f"[!] {idx+1}/{len(websites)} Skip {url} (already processed)")
            continue
        print(f"[+] Output dir: {output_dir}")

        print("\n" + "=" * 80)
        print(f"[{idx+1}/{len(websites)}] Processing: {url}")
        print("=" * 80)

        cmd1 = [
            "sudo", "tcpdump",
            "-i", BRIDGE,
            "tcp", "port", "27890",
            "and", "host", CLASH_IP,
            "-nn", "-s", "0",
            "-w", os.path.join(output_dir, "stage1_raw.pcap"),
        ]
        cmd2 = [
            "sudo", "tcpdump",
            "-i", BRIDGE,
            "host", CLASH_IP,
            "and", "not", "tcp", "port", "27890",
            "and", "not", "port", "9090",
            "and", "not", "arp",
            "-nn", "-s", "0",
            "-w", os.path.join(output_dir, "stage2_clash.pcap"),
        ]
        print("[*] Starting tcpdump...")
        p1 = start_tcpdump(cmd1)
        time.sleep(0.5)
        p2 = start_tcpdump(cmd2)
        current_processes = [p1, p2]
        PROCESSES.extend(current_processes)

        try:
            print(f"[*] Waiting {START_WAIT}s before curl...")
            time.sleep(START_WAIT)

            run_curl(url)

            print(f"[*] Waiting {END_WAIT}s after curl...")
            time.sleep(END_WAIT)
        finally:
            print("[*] Stopping tcpdump processes...")
            for p in current_processes:
                try:
                    os.killpg(os.getpgid(p.pid), signal.SIGTERM)
                except Exception:
                    pass

            time.sleep(1)

            for p in current_processes:
                try:
                    os.killpg(os.getpgid(p.pid), signal.SIGKILL)
                except Exception:
                    pass
            print("[+] tcpdump stopped.")

    print("[!] Press Ctrl+C to stop cleanly.\n")
    try:
        i = 0
        while True:
            print(f"\rWaiting... {i}", end="", flush=True)
            i += 1
            time.sleep(1)
    except KeyboardInterrupt:
        cleanup()


if __name__ == "__main__":
    """
    Example:

       echo "$(whoami) ALL=(ALL) NOPASSWD: $(which tcpdump)" | sudo tee /etc/sudoers.d/tcpdump
       sudo chmod 440 /etc/sudoers.d/tcpdump
       nohup python3 -u flowcrawl/run_tcpdump-clash_only.py \
        --output data/vless/pcap-clash_only \
        --link-file data/links-for-request/top-1000-websites.txt \
        > run_tcpdump-clash_only.log 2>&1 &
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o", "--output",
        default="data/trojan/pcap-clash_only",
        help="Directory to save pcap files"
    )
    parser.add_argument(
        "--link-file",
        default=DEFAULT_LINK_FILE,
        help="Path to website list file"
    )
    args = parser.parse_args()

    main(args.link_file, args.output)
