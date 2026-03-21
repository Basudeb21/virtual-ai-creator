# services/api/get_all_message_api.py

import httpx
import json
from pathlib import Path

from services.api.endpoints import BASE_URL, GET_ALL_MESSAGE  # ← REMOVE AUTH_TOKEN

TEST_FILE = Path("debug/test.json")


async def get_all_messages(bearer_token):  # ← ADD PARAMETER

    url = BASE_URL + GET_ALL_MESSAGE

    headers = {
        "Authorization": f"Bearer {bearer_token}",  # ← USE PARAMETER
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

        # debug save
        with TEST_FILE.open("w", encoding="utf-8") as f:
            json.dump(res_json, f, indent=4)

        return res_json