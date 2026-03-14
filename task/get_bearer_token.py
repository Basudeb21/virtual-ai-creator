#task/get_bearer_token.py
import asyncio
from services.api.bearer_token_api import get_bearer_token


creator = {
    "id": 152,
    "email": "nancy@email.com",
    "password": "Nancy@2003"
}


async def main():
    token, creator_id = await get_bearer_token(creator)
    print(f"Retrieved token for creator {creator_id}: {token}")


if __name__ == "__main__":
    asyncio.run(main())