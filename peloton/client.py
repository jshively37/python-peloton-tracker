import json
import requests
import typing as t
from urllib.error import HTTPError


ENDPOINTS = {"auth": "/auth/login"}

PELOTON_HEADERS = {"Content-Type": "application/json"}


class PelotonClient:
    def __init__(
        self, username: str, password: str, url_path: str = "https://api.onepeloton.com"
    ) -> None:
        """_summary_

        Args:
            username (str): Username for Peloton
            password (str): Password for Peloton
            url_path (str): URL prefix
        """
        self.username = username
        self.password = password
        self.url_path = url_path

    def create_session(self) -> None:
        """This function will create a Peloton API session using the
        information that was passed to the class object.
        """
        url = self.url_path + ENDPOINTS["auth"]
        payload = json.dumps(
            {"username_or_email": f"{self.username}", "password": f"{self.password}"}
        )
        self.session = requests.Session()
        self.session.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        try:
            return self.session.post(url=url, data=payload)
        except HTTPError as e:
            print(e)

    def make_request(
        self,
        endpoint: str,
        method: str = "GET",
        headers: t.Dict = PELOTON_HEADERS,
        timeout: int = 10,
    ) -> t.Dict:
        """_summary_

        Args:
            endpoint (str): URI endpoint to access
            method (str, optional): URI method. Defaults to "GET".
            headers (t.dict, optional): URI headers. Defaults to PELOTON_HEADERS.

        Returns:
            t.dict: URI response in JSON format
        """
        url = self.url_path + endpoint
        if method == "GET":
            return self.session.get(url=url, headers=headers, timeout=timeout)
        # print(response)
