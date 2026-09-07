import socket
import sys
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = BASE_DIR / "reports"


def scan_port(host: str, port: int) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)

    try:
        result = sock.connect_ex((host, port))
        return result == 0
    finally:
        sock.close()


def main():
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"

    ports = [
        80,
        443,
        3000,
        5000,
        8000,
        8080,
    ]

    REPORT_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now()
    open_ports = []

    print("=" * 50)
    print("CyberLab Reconnaissance")
    print("=" * 50)

    print(f"Target : {host}")
    print(f"Time   : {timestamp}")
    print()

    for port in ports:
        if scan_port(host, port):
            open_ports.append(port)
            print(f"[+] {host}:{port} OPEN")
        else:
            print(f"[-] {host}:{port} CLOSED")

    report_file = REPORT_DIR / "recon-002-automated-scan.md"

    with report_file.open("w") as report:
        report.write("# Recon-002 — Automated Local Port Scan\n\n")

        report.write("## Scope\n\n")
        report.write(f"Target: `{host}`\n\n")

        report.write("## Timestamp\n\n")
        report.write(f"`{timestamp}`\n\n")

        report.write("## Scanned Ports\n\n")

        for port in ports:
            status = "OPEN" if port in open_ports else "CLOSED"
            report.write(f"- `{port}` — {status}\n")

        report.write("\n## Open Ports\n\n")

        if open_ports:
            for port in open_ports:
                report.write(f"- `{port}`\n")
        else:
            report.write("No open ports detected.\n")

        report.write("\n## Notes\n\n")
        report.write(
            "This reconnaissance was performed against the local CyberLab "
            "environment owned and controlled by the researcher.\n"
        )

    print()
    print(f"[+] Report saved to: {report_file}")


if __name__ == "__main__":
    main()
