import json
import os
from datetime import datetime

FEEDBACK_FILE = "app/data/feedback.json"


def save_feedback(feedback_data):

    os.makedirs("app/data", exist_ok=True)

    # Load existing data
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    feedback_data["timestamp"] = str(datetime.utcnow())

    data.append(feedback_data)

    with open(FEEDBACK_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_all_feedback():

    if not os.path.exists(FEEDBACK_FILE):
        return []

    with open(FEEDBACK_FILE, "r") as f:
        return json.load(f)


def get_negative_feedback():

    data = get_all_feedback()

    return [f for f in data if f["rating"] == "down"]