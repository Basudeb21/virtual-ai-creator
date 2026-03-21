# task/check_unread_messages.py

import json
from pathlib import Path

from services.get_unread_message_list import get_unread_usernames
from services.api.get_messages_by_username_api import create_post
from services.api.bearer_token_api import get_bearer_token

OUTPUT_FILE = Path("memory/unread_messages.json")


async def main(creator_id):

    users = await get_unread_usernames(creator_id)
    
    print(f"\n🔍 Checking messages for creator {creator_id}")
    print(f"📋 Users with unread messages: {users}")

    # Get bearer token for this creator
    token = get_bearer_token(creator_id)
    print(f"🔐 Bearer token obtained: {token[:20]}..." if token else "❌ No token!")

    all_messages = []

    for username in users:

        response = await create_post(username, token)  # ← PASS TOKEN, NOT creator_id!

        if not response or "data" not in response:
            print(f"⚠️ No data in response for @{username}")
            continue
        chat_messages = response["data"].get("chat_message", [])
 
        for msg in chat_messages:
            if msg.get("isSeen") == 0 and msg.get("sender_id") != creator_id:  # ← USE PARAMETER

                message_data = {
                    "creator_id": creator_id,  # ← ADD THIS
                    "username": response['data']['user']['username'],
                    "sender_id": msg.get("sender_id"),
                    "message": msg.get("text")
                }

                all_messages.append(message_data)

    # Merge with existing or overwrite
    if OUTPUT_FILE.exists():
        with OUTPUT_FILE.open("r", encoding="utf-8") as f:
            try:
                existing = json.load(f)
            except:
                existing = []
    else:
        existing = []
    
    # Remove old messages from this creator, add new ones
    existing = [m for m in existing if m.get("creator_id") != creator_id]
    existing.extend(all_messages)
    
    print(f"\n📁 Total messages to save: {len(all_messages)}")

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(existing, f, indent=4)