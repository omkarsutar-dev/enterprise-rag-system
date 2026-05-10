import json
import os

FEEDBACK_FILE = "feedback_store.json"


def load_feedback():

    if not os.path.exists(FEEDBACK_FILE):
        return []

    with open(FEEDBACK_FILE, "r") as f:
        return json.load(f)


def get_feedback_score(text):

    feedbacks = load_feedback()

    score = 0

    for fb in feedbacks:
        if text in fb.get("source_text", ""):
            if fb["rating"] == "up":
                score += 1
            else:
                score -= 1

    return score