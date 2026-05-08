import argparse
import subprocess
import time
import os
import signal
from pathlib import Path


DEFAULT_LINK_FILE = "data/links-for-request/top-1000-websites.txt"
TCPDUMP_SCRIPT = "flowcrawl/run_tcpdump-clash_only.py"
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


def start_tcpdump(output_name: str):
    cmd = [
        "sudo",
        "python3",
        TCPDUMP_SCRIPT,
        "--output",
        output_name,
    ]
    print(f"[+] Starting tcpdump script: {' '.join(cmd)}")
    p = subprocess.Popen(
        cmd,
        preexec_fn=os.setsid,
    )
    print(f"[+] tcpdump pid = {p.pid}")

    return p


def stop_process_tree(proc: subprocess.Popen):
    print("[!] Stopping tcpdump script...")

    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGINT)
    except Exception as e:
        print(f"[!] Failed SIGINT: {e}")

    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        print("[!] Force killing...")
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except Exception:
            pass


def run_curl(url: str):
    cmd = [
        "curl",
        # "-L",
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
        print("\n===== STDOUT =====")
        print(result.stdout)
        print("\n===== STDERR =====")
        print(result.stderr)
    except Exception as e:
        print(f"[!] curl failed: {e}")


def main(link_file: str):
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

        dirname = sanitize_dirname(url)

        print("\n" + "=" * 80)
        print(f"[{idx+1}/{len(websites)}] Processing: {url}")
        print("=" * 80)

        tcpdump_proc = None
        try:
            tcpdump_proc = start_tcpdump(dirname)

            print(f"[*] Waiting {START_WAIT}s before curl...")
            time.sleep(START_WAIT)

            run_curl(url)

            print(f"[*] Waiting {END_WAIT}s after curl...")
            time.sleep(END_WAIT)

        except KeyboardInterrupt:
            print("[!] Interrupted by user")
            break

        except Exception as e:
            print(f"[!] Error: {e}")

        finally:
            if tcpdump_proc:
                stop_process_tree(tcpdump_proc)
            time.sleep(2)

    print("\n[✓] All done.")


if __name__ == "__main__":
    """
       sudo python3 flowcrawl/run_all_requests-clash_only.py \
        --link-file data/links-for-request/top-1000-websites.txt
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--link-file",
        default=DEFAULT_LINK_FILE,
        help="Path to website list file"
    )
    args = parser.parse_args()

    main(args.link_file)
