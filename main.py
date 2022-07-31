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

}


def api_request(slug, headers=PELOTON_HEADERS, payload=None, method="GET"):
    url = PELOTON_PATH + slug
    response = requests.request(method, url, data=payload, headers=headers)
    try:
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        print(e)


if __name__ == "__main__":

    # Creates the authentication payload.
    payload = json.dumps({
        "username_or_email": f"{PELOTON_USERNAME}",
        "password": f"{PELOTON_PASSWORD}"
        })

    # Attempt to authenticate with Peloton
    userid = api_request(
        PELOTON_SLUGS['auth'],
        PELOTON_HEADERS,
        payload=payload,
        method="POST")

    user_id = userid['user_id']
    print(user_id)
