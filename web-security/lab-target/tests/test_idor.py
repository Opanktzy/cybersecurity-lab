import requests

BASE_URL = "http://127.0.0.1:8000"


def test_user_object_access():
    for user_id in range(1, 4):
        response = requests.get(
            f"{BASE_URL}/users/{user_id}",
            timeout=5,
        )

        print(f"GET /users/{user_id} -> {response.status_code}")
        print(response.json())


if __name__ == "__main__":
    test_user_object_access()
