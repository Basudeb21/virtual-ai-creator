# task/generate_reply_from_message.py

import json
from pathlib import Path

from memory.prompt_chat_handler import chat_with_creator


INPUT_FILE = Path("memory/unread_messages.json")

CREATOR_ID = 152


def main():

    if not INPUT_FILE.exists():
        return

    with INPUT_FILE.open("r", encoding="utf-8") as f:
        messages = json.load(f)

    for msg in messages:

        user_id = msg["sender_id"]
        user_message = msg["message"]

        print("\n-----------------------------")
        print(f"User ID : {user_id}")
        print(f"User    : {user_message}")

        reply = chat_with_creator(
            creator_id=CREATOR_ID,
            user_id=user_id,
            user_message=user_message
        )

        print("AI      :", reply)


if __name__ == "__main__":
    main()