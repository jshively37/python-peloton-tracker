import os
import time

from dotenv import load_dotenv

from peloton.client import PelotonClient

load_dotenv()
PELOTON_PATH = os.environ.get("PELOTON_PATH")
PELOTON_USERNAME = os.environ.get("PELOTON_USERNAME")
PELOTON_PASSWORD = os.environ.get("PELOTON_PASSWORD")


# Need to determine why some workouts the time_seconds field is null but
# data exists in the payload.
def parse_workouts(workouts):
    for workout in workouts:
        try:
            if (
                workout["fitness_discipline"] == "cycling"
                and workout["v2_total_video_watch_time_seconds"] >= 600
            ):
                date = get_date(workout)
                print(date)
        except TypeError:
            print(workout)


def get_date(workout):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(workout["created_at"]))


if __name__ == "__main__":
    client = PelotonClient(
        username=PELOTON_USERNAME, password=PELOTON_PASSWORD, url_path=PELOTON_PATH
    )
    client.create_session()
    all_workouts = client.get_all_workouts()
    parse_workouts(all_workouts)

    print(len(all_workouts))
