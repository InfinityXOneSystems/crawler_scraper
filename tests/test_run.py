import logging

import requests


def test_run_locally():
    url = "http://127.0.0.1:8080/run"

    # Test with valid payload
    payload = {"seed_url": "https://example.com", "industry": "generic"}
    r = requests.post(url, json=payload, timeout=10)
    assert r.status_code == 200, f"Expected 200, got {r.status_code}"
    response = r.json()
    assert "content" in response, "Missing 'content' in response"
    logging.info("Test passed for valid payload.")
    assert "content_length" in response["metadata"], "Missing 'content_length' in metadata"
    logging.info("Test passed for valid payload.")

    # Test with missing seed_url
    payload = {"industry": "generic"}
    r = requests.post(url, json=payload, timeout=10)
    assert r.status_code == 400, f"Expected 400, got {r.status_code}"
    response = r.json()
    assert "error" in response, "Missing 'error' in response"
    logging.info("Test passed for missing seed_url.")

    # Test with invalid URL
    payload = {"seed_url": "invalid-url", "industry": "generic"}
    r = requests.post(url, json=payload, timeout=10)
    assert r.status_code == 400, f"Expected 400, got {r.status_code}"
    response = r.json()
    assert "error" in response, "Missing 'error' in response"
    logging.info("Test passed for invalid URL.")


if __name__ == '__main__':
    test_run_locally()
