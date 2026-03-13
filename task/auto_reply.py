import json
from pathlib import Path

from memory.prompt_chat_handler import chat_with_creator
from services.api.send_message_api import send_message_api
from memory.unread_message_manager import remove_message
from services.api.mark_chat_read_api import create_post

UNREAD_FILE = Path("memory/unread_messages.json")

AI_ID = 152


async def auto_reply():

    if not UNREAD_FILE.exists():
        print("No unread_messages.json found")
        return

    with UNREAD_FILE.open("r", encoding="utf-8") as f:
        messages = json.load(f)

    if not messages:
        print("No unread messages")
        return

    for msg in messages:

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

        # remove processed message
        user_has_more_messages = remove_message(sender_id, user_message)

        # if no more messages from this sender → mark read
        if not user_has_more_messages:
            await create_post(sender_id)