import asyncio
from services.get_unread_message_list import get_unread_usernames


async def main():

    users = await get_unread_usernames()

    print("Unread users:")
    print(users)


asyncio.run(main()) 