#workers/message_worker.py
import asyncio
import json
from pathlib import Path

from task.check_unread_messages import main as fetch_unread
from memory.prompt_chat_handler import chat_with_creator
from services.api.send_message_api import send_message_api
from services.api.mark_chat_read_api import create_post
from memory.unread_message_manager import remove_message

UNREAD_FILE = Path("memory/unread_messages.json")
USER_FILE = Path("memory/user.json")  # contains all creators
AI_ID = 152
FETCH_INTERVAL = 15  # seconds


async def load_unread_messages():
    if not UNREAD_FILE.exists():
        return []
    with UNREAD_FILE.open("r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def is_creator_online():
    """Check if the AI creator is active from user.json"""
    if not USER_FILE.exists():
        return False
    with USER_FILE.open("r", encoding="utf-8") as f:
        try:
            users = json.load(f)
        except json.JSONDecodeError:
            return False
    creator = users.get(str(AI_ID))
    if not creator:
        return False
    return creator.get("behavior", {}).get("is_active", 0) == 1


async def handle_messages():
    print("Starting Message Worker...")

    while True:

        # Check if creator is online
        if not is_creator_online():
            print(f"Creator {AI_ID} is offline. Waiting...")
            await asyncio.sleep(FETCH_INTERVAL)
            continue

        # Fetch unread messages
        try:
            await fetch_unread()
        except Exception as e:
            print("Fetch unread failed:", e)
            await asyncio.sleep(FETCH_INTERVAL)
            continue

        # Load messages
        messages = await load_unread_messages()

        if not messages:
            print("No unread messages")
            await asyncio.sleep(FETCH_INTERVAL)
            continue

        # Process messages
        for msg in messages[:]:
            username = msg["username"]
            sender_id = msg["sender_id"]
            user_message = msg["message"]

            print("\n-----------------------------")
            print(f"Username : {username}")
            print(f"User ID  : {sender_id}")
            print(f"Message  : {user_message}")

            reply = chat_with_creator(
                creator_id=AI_ID,
                user_id=sender_id,
                user_message=user_message
            )

            print("AI Reply :", reply)

            response = await send_message_api(username, reply)
            print("API Response:", response)

            user_has_more_messages = remove_message(sender_id, user_message)

            if not user_has_more_messages:
                await create_post(sender_id)
                print(f"Marked all messages from user {sender_id} as read")

        await asyncio.sleep(FETCH_INTERVAL)


if __name__ == "__main__":
    asyncio.run(handle_messages())