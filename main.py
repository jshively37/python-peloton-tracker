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
    all_workouts = client.get_all_workouts()
    print(all_workouts)
