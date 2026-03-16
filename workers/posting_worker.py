# services/posting_worker.py

import json
import time
import random
import os
import sys
import asyncio
import httpx
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from services.caption_generator import generate_caption
from config.redis_client import get_redis, REDIS_QUEUE
from services.api.bearer_token_api import get_bearer_token
from services.api.endpoints import BASE_URL, API_POST


# Reuse HTTP client for better performance
client = httpx.Client(timeout=300)


def post_to_api(media_path, creator_id):

    # Get bearer token (async fix)
    token = get_bearer_token(creator_id)

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    # Ensure media exists
    if not os.path.exists(media_path):
        print("❌ Media file not found:", media_path)
        return 400, "file_not_found"

    ext = os.path.splitext(media_path)[1].lower()

    # Caption logic
    if ext in [".mp4", ".mov", ".webm"]:
        caption = "Take a look at this 🎬"
    else:
        try:
            caption = generate_caption(media_path).strip()
        except Exception as e:
            print("⚠ Caption generation failed:", e)
            caption = "Check this out 📸"

    data = {
        "access_type": "public",
        "post_with_story": random.choice(["on", "off"]),
        "text": caption,
        "price": 0,
        "release_date": "",
        "expire_date": ""
    }

    with open(media_path, "rb") as f:

        files = {
            "attachments[0]": (
                os.path.basename(media_path),
                f,
                "application/octet-stream"
            )
        }

        res = client.post(
            BASE_URL + API_POST,
            headers=headers,
            data=data,
            files=files
        )

    return res.status_code, res.text


def main():

    print("🚀 Starting Posting Worker...")

    r = get_redis()

    while True:

        now = datetime.now().timestamp()

        jobs = r.zrangebyscore(
            REDIS_QUEUE,
            min=0,
            max=now,
            start=0,
            num=1
        )

        if not jobs:
            time.sleep(5)
            continue

        raw = jobs[0]

        # Remove job from Redis
        r.zrem(REDIS_QUEUE, raw)

        job = json.loads(raw)

        creator_id = job["creator_id"]
        media_path = job["media_url"]

        print("\n-----------------------------------")
        print(f"🚀 Posting for creator {creator_id}")
        print(f"📁 Media: {media_path}")

        # Simulate human delay
        time.sleep(random.uniform(5, 10))

        try:

            status, text = post_to_api(media_path, creator_id)

            print("📤 API Status:", status)
            print("📤 API Body:", text)

            try:
                result = json.loads(text)
            except:
                result = {}

            if status == 200 and result.get("status") != False:
                print("✅ Post completed")

            else:
                print("❌ API rejected post:", result)

        except Exception as e:
            print("❌ Worker error:", e)


if __name__ == "__main__":
    main()