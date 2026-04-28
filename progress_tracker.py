import json
import os
from datetime import datetime

DATA_FILE = "user_progress.json"

def load_progress():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"mistakes": [], "weekly_summaries": []}

def save_progress(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def log_mistake(mistake_description):
    data = load_progress()
    data["mistakes"].append({
        "date": str(datetime.now().date()),
        "description": mistake_description
    })
    save_progress(data)

def get_recent_mistakes(limit=5):
    data = load_progress()
    return "\n".join([m["description"] for m in data["mistakes"][-limit:]])