# services/api/get_messages_by_username_api.py

import httpx
import json
from pathlib import Path
from services.api.endpoints import BASE_URL, GET_MESSAGES_BY_USERNAME  # ← REMOVE AUTH_TOKEN

TEST_FILE = Path("debug/test1.json")


async def create_post(username: str, bearer_token):  # ← ADD PARAMETER
    url = BASE_URL + GET_MESSAGES_BY_USERNAME.format(uid=username)

    headers = {
        "Authorization": f"Bearer {bearer_token}",  # ← USE PARAMETER
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=url,
            headers=headers,
            json={}
        )

        res_json = response.json()

        with TEST_FILE.open("w", encoding="utf-8") as f:
            json.dump(res_json, f, indent=4)

        return res_json