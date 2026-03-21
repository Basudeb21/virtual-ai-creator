# services/api/send_message_api.py

import httpx
import json
from pathlib import Path

from services.api.endpoints import BASE_URL, SEND_MESSAGE, AUTH_TOKEN

TEST_FILE = Path("debug/test_sent_msg.json")


async def send_message_api(username, body=None, image_path=None):

    url = BASE_URL + SEND_MESSAGE.format(uid=username)

    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        # ❗ DO NOT set Content-Type manually
    }

    data = {
        "price": "0"
    }

    print("\n------ API DEBUG ------")
    print("URL:", url)
    print("BODY:", body)
    print("IMAGE:", image_path)
    print("-----------------------\n")

    async with httpx.AsyncClient(timeout=60) as client:

        # 🖼️ IMAGE MESSAGE
        if image_path:
            with open(image_path, "rb") as file:
                files = {
                    "attachment": (
                        Path(image_path).name,
                        file,
                        "image/jpeg"
                    )
                }

                response = await client.post(
                    url=url,
                    headers=headers,
                    data=data,
                    files=files
                )

        # 📝 TEXT MESSAGE
        else:
            if body:
                data["message"] = body

            response = await client.post(
                url=url,
                headers=headers,
                data=data
            )

        res_json = response.json()

        print("STATUS:", response.status_code)
        print("RESPONSE:", res_json)

        with TEST_FILE.open("w", encoding="utf-8") as f:
            json.dump(res_json, f, indent=4)

        return res_json