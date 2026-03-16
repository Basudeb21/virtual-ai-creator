#services/post_scheduler.py
import random
import json
import os
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler

from config.redis_client import get_redis, REDIS_QUEUE

USER_FILE = "memory/user.json"
IMG_DIR = "attachments/imgs"
VIDEO_DIR = "attachments/videos"


def load_active_creators():
    if not os.path.exists(USER_FILE):
        return {}

    with open(USER_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def random_time():
    now = datetime.now()
    delay = random.randint(3, 5)
    scheduled = now + timedelta(minutes=delay)
    return scheduled.replace(second=0, microsecond=0)


def get_all_media():

    images = []
    videos = []

    if os.path.exists(IMG_DIR):
        images = [
            f"{IMG_DIR}/{f}"
            for f in os.listdir(IMG_DIR)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ]

    if os.path.exists(VIDEO_DIR):
        videos = [
            f"{VIDEO_DIR}/{f}"
            for f in os.listdir(VIDEO_DIR)
            if f.lower().endswith((".mp4", ".mov", ".webm"))
        ]

    return images + videos


def schedule_posts():

    r = get_redis()

    creators = load_active_creators()

    if not creators:
        print("No active creators found")
        return

    all_media = get_all_media()

    if not all_media:
        print("No media found")
        return

    for creator_id, creator in creators.items():

        behavior = creator.get("behavior", {})

        if behavior.get("is_active") != 1:
            continue

        posting_frequency = behavior.get("posting_frequency", 1)

        print(f"\nCreator {creator_id} scheduling {posting_frequency} posts")

        available_media = all_media.copy()

        for _ in range(posting_frequency):

            if not available_media:
                break

            media = random.choice(available_media)
            available_media.remove(media)

            scheduled_time = random_time()

            job = {
                "creator_id": int(creator_id),
                "media_url": media,
                "scheduled_time": scheduled_time.isoformat()
            }

            score = scheduled_time.timestamp()

            r.zadd(REDIS_QUEUE, {json.dumps(job): score})

            print(
                f"📅 Scheduled post for creator {creator_id} at {scheduled_time}"
            )

    print("\n✅ Scheduler cycle complete\n")


scheduler = BlockingScheduler()

scheduler.add_job(
    schedule_posts,
    "interval",
    hours=1,
    next_run_time=datetime.now()
)

scheduler.start()