# services/api/mark_chat_read_api.py

import httpx
from pathlib import Path
from services.api.endpoints import BASE_URL, MARK_AS_READ, AUTH_TOKEN

TEST_FILE = Path("test1.json")


async def create_post(user_id: str):
    url = BASE_URL + MARK_AS_READ


    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

    body = {'user_id' : user_id}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=url,
            headers=headers,
            json=body
        )

        res_json = response.json()
        print('Mark AS READ :: ',res_json)