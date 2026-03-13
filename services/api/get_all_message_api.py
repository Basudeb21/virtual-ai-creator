# services/api/get_message_api.py
import httpx
import asyncio
import json
from pathlib import Path
from endpoints import BASE_URL, GET_ALL_MESSAGE, AUTH_TOKEN

TEST_FILE = Path("test.json")

async def create_post():
    url = BASE_URL + GET_ALL_MESSAGE
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=url,
            headers=headers,
            json=data
        )

        res_json = response.json()
        with TEST_FILE.open("w", encoding="utf-8") as f:
            json.dump(res_json, f, indent=4)


asyncio.run(create_post())