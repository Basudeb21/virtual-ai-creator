# services/get_unread_message_list.py
from services.api.get_all_message_api import get_all_messages
from services.api.bearer_token_api import get_bearer_token


async def get_unread_usernames(creator_id):

    # Get bearer token for this creator
    token = get_bearer_token(creator_id)
    
    response = await get_all_messages(token)

    unread_users = []

    for user in response.get("data", []):
        if user.get("unread_msg_count", 0) > 0:
            unread_users.append(user.get("username"))

    return unread_users