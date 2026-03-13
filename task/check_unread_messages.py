# task/check_unread_messages.py

import asyncio
import json
from pathlib import Path

# from services.get_unread_message_list import get_unread_usernames
from services.get_unread_message_list import get_unread_usernames
from services.api.get_messages_by_username_api import create_post

OUTPUT_FILE = Path("memory/unread_messages.json")

AI_ID = 152


async def main():

    users = await get_unread_usernames()

    print("Unread users:")
    print(users)

    all_messages = []

    for username in users:

        response = await create_post(username)

        if not response or "data" not in response:
            continue
        print(response['data']['user']['username'])
        chat_messages = response["data"].get("chat_message", [])
 
        for msg in chat_messages:

            if msg.get("isSeen") == 0 and msg.get("sender_id") != AI_ID:

                message_data = {
                    "username": response['data']['user']['username'],
                    "sender_id": msg.get("sender_id"),
                    "message": msg.get("text")
                }

                all_messages.append(message_data)

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(all_messages, f, indent=4)

    print("Messages saved to memory/unread_messages.json")
