import datetime
import os

from dotenv import load_dotenv

from peloton.client import PelotonClient


load_dotenv()
PELOTON_PATH = os.environ.get("PELOTON_PATH")
PELOTON_USERNAME = os.environ.get("PELOTON_USERNAME")
PELOTON_PASSWORD = os.environ.get("PELOTON_PASSWORD")


def parse_pr_workout(workout):
    pr_dict_values = {"workout_time": format_data_time(workout["created_at"])}
    response = client.get_workout_detail(workout["id"])
    for summary in response["summaries"]:
        pr_dict_values |= parse_summary_dict(summary)
    return {response["duration"] / 60: pr_dict_values}


def format_data_time(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime("%Y-%m-%d %H:%M:%S")


def parse_summary_dict(summary):
    pr_dict_values = {}
    if summary["display_name"].lower() == "distance":
        miles = summary["value"]
        pr_dict_values["miles"] = miles
    elif summary["display_name"].lower() == "calories":
        calories = summary["value"]
        pr_dict_values["calories"] = calories
    elif summary["display_name"].lower() == "total output":
        output = summary["value"]
        pr_dict_values["output"] = output
    return pr_dict_values


if __name__ == "__main__":
    client = PelotonClient(
        username=PELOTON_USERNAME, password=PELOTON_PASSWORD, url_path=PELOTON_PATH
    )
    client.create_session()
    all_workouts = client.get_all_workouts()

    pr_list = []
    for workout in all_workouts:
        if workout["is_total_work_personal_record"]:
            pr_workout = parse_pr_workout(workout)
            pr_list.append(pr_workout)
    print(pr_list)
