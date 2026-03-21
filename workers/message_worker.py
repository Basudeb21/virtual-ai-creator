# workers/message_worker.py
import asyncio
import json
import time
from pathlib import Path

from task.check_unread_messages import main as fetch_unread
from memory.prompt_chat_handler import chat_with_creator
from services.api.send_message_api import send_message_api
from services.api.mark_chat_read_api import create_post
from memory.unread_message_manager import remove_message
from queues.queue_manager import push_msg
from services.api.bearer_token_api import get_bearer_token 

UNREAD_FILE = Path("memory/unread_messages.json")
USER_FILE = Path("memory/user.json")  
FETCH_INTERVAL = 15 


async def load_unread_messages(creator_id):
    if not UNREAD_FILE.exists():
        return []
    with UNREAD_FILE.open("r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            # Filter messages for this creator
            return [msg for msg in data if msg.get("creator_id") == creator_id]
        except json.JSONDecodeError:
            return []

def get_all_online_creators():
    if not USER_FILE.exists():
        return {}
    with USER_FILE.open("r", encoding="utf-8") as f:
        try:
            users = json.load(f)
        except json.JSONDecodeError:
            return {}
    return {int(cid): data for cid, data in users.items() 
            if data.get("behavior", {}).get("is_active", 0) == 1}


async def handle_messages():
    print("Starting Message Worker...")

    while True:
        online_creators = get_all_online_creators()

        if not online_creators:
            print("No creators online. Waiting...")
            await asyncio.sleep(FETCH_INTERVAL)
            continue

        # Process each online creator
        for creator_id, creator_data in online_creators.items():
            try:
                await fetch_unread(creator_id)  # ← PASS creator_id
            except Exception as e:
                print(f"Fetch unread failed for creator {creator_id}:", e)
                continue

            messages = await load_unread_messages(creator_id)  # ← PASS creator_id

            if not messages:
                print(f"No messages for creator {creator_id}")
                continue

            # Get bearer token for this creator
            try:
                token = get_bearer_token(creator_id)
            except Exception as e:
                print(f"Failed to get token for creator {creator_id}:", e)
                continue

            for msg in messages[:]:
                username = msg["username"]
                sender_id = msg["sender_id"]
                user_message = msg["message"]

                print("\n******************************")
                print(f"Creator ID: {creator_id}")
                print(f"Username : {username}")
                print(f"User ID  : {sender_id}")
                print(f"Message  : {user_message}")
                print("******************************\n")

                push_msg({
                    "ai_id": creator_id,  # ← USE LOOP creator_id
                    "fan_id": sender_id,
                    "message": user_message,
                    "created_at": int(time.time())
                })

                reply = chat_with_creator(
                    creator_id=creator_id,  # ← USE LOOP creator_id
                    user_id=sender_id,
                    user_message=user_message
                )

                response = await send_message_api(username, reply, token)  # ← PASS token
                print("API Response:", response)

                user_has_more_messages = remove_message(sender_id, user_message)

                if not user_has_more_messages:
                    await create_post(sender_id, token)  # ← PASS token
                    print(f"Marked all messages from user {sender_id} as read")

        await asyncio.sleep(FETCH_INTERVAL)


if __name__ == "__main__":
    asyncio.run(handle_messages())