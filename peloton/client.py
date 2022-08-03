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


FITNESS_DISCIPLINE = {"cycling": "cycling"}


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
            user_id = self.session.post(url=url, data=payload).json()
            self.user_id = user_id["user_id"]
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
        elif method == "POST":
            return self.session.post(url=url, headers=headers, timeout=timeout)
        elif method == "PUT":
            return self.session.put(url=url, headers=headers, timeout=timeout)

    def get_all_workouts(self) -> None:
        """Return all workouts from the API.
        """
        self.all_workouts = self.make_request(
            f"{ENDPOINTS['general_user']}/{self.user_id}/workouts"
        ).json()

    def parse_all_workouts(self) -> None:
        """Create a list of workout IDs based upon activity requested.
        """
        self.workout_ids = [
            workout["id"]
            for workout in self.all_workouts["data"]
            if workout["fitness_discipline"] == FITNESS_DISCIPLINE["cycling"]
        ]

    def get_workout_detail(self) -> None:
        """Return specific information on all workouts captured in the
            workout list.
        """
        for workout in self.workout_ids:
            get_workout_details = self.make_request(
                f"{ENDPOINTS['general_workout']}/{workout}/performance_graph"
            ).json()
            for summary in get_workout_details["summaries"]:
                print(summary)
