import os

from dotenv import load_dotenv

from peloton.client import PelotonClient

load_dotenv()
PELOTON_PATH = os.environ.get("PELOTON_PATH")
PELOTON_USERNAME = os.environ.get("PELOTON_USERNAME")
PELOTON_PASSWORD = os.environ.get("PELOTON_PASSWORD")


if __name__ == "__main__":
    client = PelotonClient(
        username=PELOTON_USERNAME, password=PELOTON_PASSWORD, url_path=PELOTON_PATH
    )
    client.create_session()
    client.get_all_workouts()
    client.parse_all_workouts()
    # Need to loop through workout detail
    # workout_detail = client.get_workout_detail()
    # print(workout_detail)
