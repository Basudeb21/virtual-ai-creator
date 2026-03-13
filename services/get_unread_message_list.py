# services/get_unread_message_list.py
from services.api.get_all_message_api import get_all_messages


async def get_unread_usernames():

    response = await get_all_messages()

    unread_users = []

    for user in response.get("data", []):
        if user.get("unread_msg_count", 0) > 0:
            unread_users.append(user.get("username"))

    return unread_users