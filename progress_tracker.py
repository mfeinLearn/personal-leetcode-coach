import json
import os
from datetime import datetime

DATA_FILE = "user_progress.json"

def load_progress():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                content = f.read().strip()
                if not content:  # File is empty
                    return {"mistakes": [], "weekly_summaries": []}
                return json.loads(content)
        except json.JSONDecodeError:
            # File is corrupted or empty
            return {"mistakes": [], "weekly_summaries": []}
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