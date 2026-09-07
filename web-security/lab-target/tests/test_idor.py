import requests

BASE_URL = "http://127.0.0.1:8000"

HEADERS = {
    "X-Token": "alice-token"
}


def test_own_object():
    response = requests.get(
        f"{BASE_URL}/users/1",
        headers=HEADERS,
        timeout=5,
    )

    print("[+] Alice accessing Alice")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")


def test_other_object():
    response = requests.get(
        f"{BASE_URL}/users/2",
        headers=HEADERS,
        timeout=5,
    )

    print("\n[+] Alice accessing Bob")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")


if __name__ == "__main__":
    test_own_object()
    test_other_object()
