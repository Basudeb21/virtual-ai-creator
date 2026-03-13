# workers/creator_activity_worker.py

import time as t
from datetime import datetime, time, timedelta
from database.db import db
from services.creator_loader import load_creator
from memory.active_creators import add_creator, remove_creator, get_all_creators


def to_time(val):
    """
    Converts MySQL TIME (timedelta) or seconds (int/float) to datetime.time
    """
    if isinstance(val, time):
        return val
    elif isinstance(val, timedelta):
        total_seconds = val.total_seconds()
    elif isinstance(val, (int, float)):
        total_seconds = float(val)
    else:
        return None

    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    return time(hour=hours, minute=minutes, second=seconds)


def check_creators():
    query = """
        SELECT user_id, online_time, offline_time
        FROM ai_creator_behavior
        WHERE is_active = 1
    """
    creators = db.fetch_all(query)
    now = datetime.now().time()

    for creator in creators:
        user_id = creator["user_id"]
        online = to_time(creator["online_time"])
        offline = to_time(creator["offline_time"])

        if not online or not offline:
            continue

        # Case 1: online and offline on same day
        if online <= offline:
            is_active_now = online <= now <= offline
        else:
            # Case 2: crosses midnight
            is_active_now = now >= online or now <= offline

        if is_active_now:
            if user_id not in get_all_creators():
                data = load_creator(user_id)
                add_creator(user_id, data)
                print(f"[ONLINE] Creator {user_id} is now active")
        else:
            if user_id in get_all_creators():
                remove_creator(user_id)
                print(f"[OFFLINE] Creator {user_id} is now inactive")

def run_worker():
    print("Starting Creator Activity Worker...")
    while True:
        try:
            check_creators()
        except Exception as e:
            print(f"[ERROR] check_creators failed: {e}")
        t.sleep(30)