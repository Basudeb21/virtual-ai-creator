import json
from pathlib import Path

UNREAD_FILE = Path("memory/unread_messages.json")


def remove_message(sender_id, message):

    if not UNREAD_FILE.exists():
        return False

    with UNREAD_FILE.open("r", encoding="utf-8") as f:
        messages = json.load(f)

    updated_messages = [
        msg for msg in messages
        if not (
            msg["sender_id"] == sender_id and
            msg["message"] == message
        )
    ]

    with UNREAD_FILE.open("w", encoding="utf-8") as f:
        json.dump(updated_messages, f, indent=4)

    user_has_messages = any(
        msg["sender_id"] == sender_id
        for msg in updated_messages
    )

    return user_has_messages