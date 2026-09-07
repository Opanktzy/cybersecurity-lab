from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

LOG_FILE = BASE_DIR / "logs" / "access.log"
ALERT_FILE = BASE_DIR / "logs" / "security-alerts.log"


def load_rules():
    rules = {}

    rule_file = BASE_DIR / "rules" / "rules.txt"

    with rule_file.open() as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            name, pattern = line.split("=", 1)
            rules[name] = pattern

    return rules


def analyze_logs():
    rules = load_rules()

    alerts = []

    with LOG_FILE.open() as file:
        for line_number, line in enumerate(file, start=1):
            for rule_name, pattern in rules.items():

                if pattern.lower() in line.lower():

                    alert = {
                        "line": line_number,
                        "rule": rule_name,
                        "evidence": line.strip(),
                    }

                    alerts.append(alert)

    return alerts


def save_alerts(alerts):
    with ALERT_FILE.open("w") as file:

        for alert in alerts:
            file.write(
                f"[ALERT] "
                f"rule={alert['rule']} "
                f"line={alert['line']} "
                f"evidence={alert['evidence']}\n"
            )

def detect_repeated_forbidden():
    forbidden_count = 0

    with LOG_FILE.open() as file:
        for line in file:
            if " 403" in line:
                forbidden_count += 1

    if forbidden_count >= 2:
        return {
            "rule": "REPEATED_FORBIDDEN_ACCESS",
            "count": forbidden_count,
        }

    return None
def main():
    print("=" * 60)
    print("CyberLab Mini-SOC")
    print("=" * 60)

    print(f"Log: {LOG_FILE}")

    alerts = analyze_logs()

    print(f"\n[+] Alerts detected: {len(alerts)}")

    for alert in alerts:
        print(
            f"[ALERT] "
            f"{alert['rule']} "
            f"-> {alert['evidence']}"
        )

    save_alerts(alerts)

    print(f"\n[+] Alerts saved to: {ALERT_FILE}")


if __name__ == "__main__":
    main()
