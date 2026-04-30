import json
import os
from datetime import datetime

GOALS_FILE = "user_goals.json"

def load_goals():
    if os.path.exists(GOALS_FILE):
        with open(GOALS_FILE, "r") as f:
            return json.load(f)
    return {"current_goal": "Graphs", "last_updated": str(datetime.now().date())}

def save_goal(new_goal):
    data = {"current_goal": new_goal, "last_updated": str(datetime.now().date())}
    with open(GOALS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def should_ask_new_goal():
    data = load_goals()
    last = datetime.strptime(data["last_updated"], "%Y-%m-%d")
    return (datetime.now() - last).days >= 30