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
    get_user_id = client.create_session().json()

    # Get all workouts
    get_all_workouts = client.make_request(
        f"/api/user/{get_user_id['user_id']}/workouts"
    ).json()

    # Parse out workout IDs
    workouts_list = [workout["id"] for workout in get_all_workouts["data"]]

    for workout in workouts_list:
        get_workout_detail = client.make_request(
            f"/api/workout/{workout}/performance_graph"
        ).json()
        for x in get_workout_detail["summaries"]:
            print(x)
