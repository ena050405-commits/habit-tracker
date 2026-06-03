import json
import datetime
import os
import sys
import requests
from zoneinfo import ZoneInfo

PUSHOVER_TOKEN = os.environ.get("PUSHOVER_TOKEN")
PUSHOVER_USER = os.environ.get("PUSHOVER_USER")

if not PUSHOVER_TOKEN or not PUSHOVER_USER:
    print("No credentials")
    sys.exit(1)

def send_push(title, message):
    try:
        requests.post("https://api.pushover.net/1/messages.json", data={
            "token": PUSHOVER_TOKEN,
            "user": PUSHOVER_USER,
            "title": title,
            "message": message
        }, timeout=10)
    except Exception as e:
        print(f"Error: {e}")

def main():
    with open("habits.json", "r") as f:
        data = json.load(f)
    now = datetime.datetime.now(ZoneInfo("Europe/Moscow"))
    modified = False
    for habit in data["habits"]:
        if not habit.get("enabled", True):
            continue
        last = datetime.datetime.fromisoformat(habit["last_check"])
        if (now - last).total_seconds() / 3600 >= habit["interval_hours"]:
            send_push(f"Reminder: {habit['name']}", f"Time! {habit['interval_hours']} hours passed")
            habit["last_check"] = now.isoformat()
            modified = True
    if modified:
        with open("habits.json", "w") as f:
            json.dump(data, f, indent=2)
        os.system("git config user.name 'bot'")
        os.system("git config user.email 'bot@example.com'")
        os.system("git add habits.json")
        os.system("git commit -m 'auto update' || true")
        os.system("git push")

if __name__ == "__main__":
    main()
