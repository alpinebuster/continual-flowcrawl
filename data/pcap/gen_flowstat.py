"""
CLI:
   `path_to/darkflow/target/release/darkflow --header -f darkflow -o csv --export-path /home/data/workspaces/workspace/doctoral/anonymity/_code/multicrypted_traffic_analysis/data/tor_over_vpn/Tor/20250702_124343.csv  pcap /home/data/workspaces/workspace/doctoral/anonymity/_code/multicrypted_traffic_analysis/data/tor_over_vpn/Tor/20250702_124343.pcap`
"""

import subprocess
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import os

BASE_DIR = Path(__file__).resolve().parent
# DARKFLOW_BIN = Path("../continual_darkflow/target/release/darkflow").resolve()
DARKFLOW_BIN = Path("/home/data/workspaces/workspace/doctoral/anonymity/_code/imbalanced_traffic_classification/darkflow/target/release/darkflow").resolve()
# basic, cic, cidds, darkflow, nfstream, rustiflow (NTLFlow)
FEATURE_TYPES = ["basic", "cic", "cidds", "darkflow", "nfstream", "rustiflow"]


def process_pcap(pcap_file: Path, fe_type: str):
    csv_path = pcap_file.with_name(fe_type+ "-" + pcap_file.stem + ".csv")

    cmd = [
        str(DARKFLOW_BIN),
        "--header",
        "-f", fe_type,
        "-o", "csv",
        "--export-path", str(csv_path),
        "pcap",
        str(pcap_file),
    ]

    try:
        subprocess.run(cmd, check=True)
        return f"OK: {pcap_file}"
    except subprocess.CalledProcessError as e:
        return f"ERROR: {pcap_file} -> {e}"


def main():
    pcap_files = [
        p for p in BASE_DIR.rglob("*")
        if p.suffix.lower() in [".pcap", ".pcapng"]
    ]
    print(f"Found {len(pcap_files)} pcap files")

    # All tasks: pcap × feature
    tasks = [
        (pcap, fe_type)
        for pcap in pcap_files
        for fe_type in FEATURE_TYPES
    ]

    cpus = os.cpu_count()
    assert cpus is not None
    # workers = cpus-1
    workers = cpus//2
    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(process_pcap, pcap, fe_type)
            for pcap, fe_type in tasks
        ]
        for f in as_completed(futures):
            print(f.result())


if __name__ == "__main__":
    main()
