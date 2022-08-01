import json
import os
from urllib.error import HTTPError

# Ensure requests is installed
try:
    import requests
except ImportError:
    print("requests not found")

try:
    from dotenv import load_dotenv
    load_dotenv()
    PELOTON_PATH = os.environ.get("PELOTON_PATH")
    PELOTON_USERNAME = os.environ.get("PELOTON_USERNAME")
    PELOTON_PASSWORD = os.environ.get("PELOTON_PASSWORD")
except ImportError:
    print("python-dotenv not found")

# Dictionary of Peloton API Endpoints
PELOTON_SLUGS = {
    "auth": "/auth/login"
}

# Headers for interacting with Peloton API
PELOTON_HEADERS = {
    'Content-Type': 'application/json'
}


def api_request(slug, headers=PELOTON_HEADERS, payload=None, method="GET"):
    url = PELOTON_PATH + slug
    response = requests.request(method, url, data=payload, headers=headers)
    try:
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        print(e)


def auth_request():
    payload = json.dumps({
        "username_or_email": f"{PELOTON_USERNAME}",
        "password": f"{PELOTON_PASSWORD}"
        })
    user_id = api_request(
                PELOTON_SLUGS['auth'],
                PELOTON_HEADERS,
                payload=payload,
                method="POST")
    return user_id['user_id']


if __name__ == "__main__":

    user_id = auth_request()
    print(user_id)
