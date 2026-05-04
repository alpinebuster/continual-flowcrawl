#!/usr/bin/env python3

import subprocess
import signal
import sys
import time
import os
import argparse

PROCESSES = [] # type:ignore


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


def main(output_dir):
    """
    sudo python3 flowcrawl/run_tcpdump.py --output check.torproject.org
    pgrep -a tcpdump
    curl -x socks5h://127.0.0.1:9050 'https://check.torproject.org/api/ip'
    tcpdump -r ./data/pcap/stage3_clash.pcap
    """
    os.makedirs(output_dir, exist_ok=True)
    print(f"[+] Output dir: {output_dir}")

    print("[*] Fetching container info...")

    TOR_IP = get_container_ip("tor")
    CLASH_IP = get_container_ip("clash")
    NETWORK_NAME = "continual-flowcrawl_clashnet"
    BRIDGE = get_bridge_name(NETWORK_NAME)
    SUBNET = get_subnet(NETWORK_NAME)

    print(f"[+] TOR_IP   = {TOR_IP}")
    print(f"[+] CLASH_IP = {CLASH_IP}")
    print(f"[+] BRIDGE   = {BRIDGE}")
    print(f"[+] SUBNET   = {SUBNET}")


    cmd1 = [
        "sudo", "tcpdump",
        "-i", BRIDGE,
        "tcp", "port", "9050",
        "and", "host", TOR_IP,
        "and", "not", "host", CLASH_IP,
        "-nn", "-s", "0",
        "-w", os.path.join(output_dir, "stage1_raw.pcap"),
    ]

    cmd2 = [
        "sudo", "tcpdump",
        "-i", BRIDGE,
        "host", TOR_IP, "and", "host", CLASH_IP,
        "-nn", "-s", "0",
        "-w", os.path.join(output_dir, "stage2_tor.pcap"),
    ]

    cmd3 = [
        "sudo", "tcpdump",
        "-i", BRIDGE,
        "host", CLASH_IP,
        "and", "not", "host", TOR_IP,
        # "and not net", SUBNET,
        "-nn", "-s", "0",
        "-w", os.path.join(output_dir, "stage3_clash.pcap"),
    ]

    # import pdb;pdb.set_trace()
    print("[*] Starting captures...")
    PROCESSES.append(start_tcpdump(cmd1))
    time.sleep(0.5)

    PROCESSES.append(start_tcpdump(cmd2))
    time.sleep(0.5)

    PROCESSES.append(start_tcpdump(cmd3))

    print("\n[✓] All tcpdump processes started.")
    print("[!] Press Ctrl+C to stop.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        cleanup()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o", "--output",
        default="./data/pcap/check.torproject.org/",
        help="Directory to save pcap files"
    )
    args = parser.parse_args()

    main(args.output)
