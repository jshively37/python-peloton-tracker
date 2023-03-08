import json
import requests
import typing as t
from urllib.error import HTTPError


ENDPOINTS = {
    "auth": "/auth/login",
    "general_user": "/api/user",
    "general_workout": "/api/workout",
    "ride": "/api/ride"
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
        payload = json.dumps(
            {"username_or_email": f"{self.username}", "password": f"{self.password}"}
        )
        self.session = requests.Session()
        self.session.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        try:
            user_id = self.make_request(
                endpoint=ENDPOINTS["auth"], method="POST", data=payload
            )
            self.user_id = user_id["user_id"]
        except HTTPError:
            return {}

    def make_request(
        self,
        endpoint: str,
        method: str = "GET",
        headers: t.Dict = PELOTON_HEADERS,
        timeout: int = 10,
        data: t.Dict = None,
    ) -> t.Dict:
        """Function that handles making API requests.

        Args:
            endpoint (str): URI endpoint to access
            method (str, optional): URI method. Defaults to "GET".
            headers (t.dict, optional): URI headers. Defaults to PELOTON_HEADERS.
            timeout (int, optional): URI Timeout.
            limit (int, optional): Number of entries to return.
        Returns:
            t.dict: URI response in JSON format
        """
        url = self.url_path + endpoint
        try:
            return self.session.request(
                method=method, url=url, headers=headers, timeout=timeout, data=data
            ).json()
        except HTTPError:
            return {}

    def get_all_workouts(self, page: int = 0, limit: int = 100) -> t.List:
        """Return all workouts from the API.

        Args:
            page: Page to start at (default is 0)
            limit: Number of entries to return in each request (current max is 100)
        Returns:
            t.List: List of dictionaries containing all workouts
        """

        more_pages = True
        workout_list = []

        while more_pages:
            response = self.make_request(
                f"{ENDPOINTS['general_user']}/{self.user_id}/workouts?limit={limit}&page={page}"
            )
            workout_list.append(response["data"])
            if response["show_next"]:
                page += 1
            else:
                more_pages = False

        # Return a flatten list
        return [item for sublist in workout_list for item in sublist]

    def get_workout_performance_graph(self, workout_id: str) -> t.Dict:
        """Return information on a specific workout using the workout_id

        Args:
            workout_id (str): Peloton ID of the specific workout.

        Returns:
            t.Dict: json object containing workout data.
        """
        return self.make_request(
            f"{ENDPOINTS['general_workout']}/{workout_id}/performance_graph"
        )

    def get_workout_details(self, workout_id: str) -> t.Dict:
        """Returns the workout details for a specific workout using the workout_id

        Args:
            workout_id (str):
            workout_id (str):

        Returns:
            t.Dict: json object containing workout data.
        """
        return self.make_request(
            f"{ENDPOINTS['ride']}/{workout_id}/details"
        )
