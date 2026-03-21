# services/api/send_message_api.py

import httpx
import json
from pathlib import Path

from services.api.endpoints import BASE_URL, SEND_MESSAGE  # ← REMOVE AUTH_TOKEN

TEST_FILE = Path("debug/test_sent_msg.json")


async def send_message_api(username, body, bearer_token):  # ← ADD PARAMETER

    url = BASE_URL + SEND_MESSAGE.format(uid=username)

    headers = {
        "Authorization": f"Bearer {bearer_token}",  # ← USE PARAMETER
        "Content-Type": "application/json"
    }

    data = {
        "message": body
    }

    print("\n------ API DEBUG ------")
    print("URL:", url)
    print("DATA:", data)
    print("-----------------------\n")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=url,
            headers=headers,
            json=data
        )

        res_json = response.json()

        print("STATUS:", response.status_code)
        print("RESPONSE:", res_json)

        with TEST_FILE.open("w", encoding="utf-8") as f:
            json.dump(res_json, f, indent=4)

        return res_json