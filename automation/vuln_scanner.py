import requests
import sys


BASE_URL = (
    sys.argv[1]
    if len(sys.argv) > 1
    else "http://127.0.0.1:8000"
)


def check_security_headers():
    print("\n[*] Checking security headers...")

    response = requests.get(
        BASE_URL,
        timeout=5,
    )

    security_headers = [
        "Content-Security-Policy",
        "X-Content-Type-Options",
        "X-Frame-Options",
        "Strict-Transport-Security",
    ]

    findings = []

    for header in security_headers:
        if header in response.headers:
            print(f"[+] {header}: PRESENT")
        else:
            print(f"[-] {header}: MISSING")
            findings.append(header)

    return findings

def check_api_endpoints():
    print("\n[*] Checking known lab endpoints...")

    endpoints = [
        "/",
        "/health",
        "/users",
        "/products",
        "/ping",
    ]

    for endpoint in endpoints:
        try:
            response = requests.get(
                BASE_URL + endpoint,
                timeout=5,
            )

            print(
                f"{endpoint:<15} "
                f"HTTP {response.status_code}"
            )

        except requests.RequestException as error:
            print(f"{endpoint:<15} ERROR: {error}")


def main():
    print("=" * 50)
    print("CyberLab Vulnerability Scanner")
    print("=" * 50)

    print(f"Target: {BASE_URL}")

    missing_headers = check_security_headers()

    check_api_endpoints()

    print("\n[*] Scan Summary")

    if missing_headers:
        print(
            f"[!] {len(missing_headers)} "
            "security headers missing"
        )
    else:
        print("[+] Security headers look good")
if __name__ == "__main__":
    main()
