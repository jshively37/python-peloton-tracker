import json
import requests
import typing as t
from urllib.error import HTTPError


ENDPOINTS = {
    "auth": "/auth/login",
    "general_user": "/api/user",
    "general_workout": "/api/workout",
}

PELOTON_HEADERS = {"Content-Type": "application/json"}


class PelotonClient:
    def __init__(
        self, username: str, password: str, url_path: str = "https://api.onepeloton.com"
    ) -> None:
        """Peloton Client that will handle making API calls to the Peloton API.

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
            user_id = self.session.post(url=url, data=payload).json()
            self.user_id = user_id["user_id"]
        except HTTPError:
            return {}

    def make_request(
        self,
        endpoint: str,
        method: str = "GET",
        headers: t.Dict = PELOTON_HEADERS,
        timeout: int = 10,
    ) -> t.Dict:
        """Function that handles making API requests.

        Args:
            endpoint (str): URI endpoint to access
            method (str, optional): URI method. Defaults to "GET".
            headers (t.dict, optional): URI headers. Defaults to PELOTON_HEADERS.

        Returns:
            t.dict: URI response in JSON format
        """
        url = self.url_path + endpoint
        try:
            return self.session.request(
                method=method, url=url, headers=headers, timeout=timeout
            )
        except HTTPError:
            return {}

    def get_all_workouts(self) -> t.Dict:
        """Return all workouts from the API.

        Returns:
            t.Dict: json object containing all the workout information.
        """
        return self.make_request(
            f"{ENDPOINTS['general_user']}/{self.user_id}/workouts"
        ).json()

    def get_workout_detail(self, workout_id: str) -> None:
        """Return information on a specific workout_id"""
        return self.make_request(
            f"{ENDPOINTS['general_workout']}/{workout_id}/performance_graph"
        ).json()
