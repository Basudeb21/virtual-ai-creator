import httpx
from services.api.endpoints import BASE_URL, API_LOGIN
from database.token_queries import save_token, get_token


def login_and_save_token(creator):

    login_url = BASE_URL + API_LOGIN

    with httpx.Client(timeout=20) as client:
        res = client.post(
            login_url,
            json={
                "email_username": creator["email"],
                "password": creator["password"]
            }
        )

    print(f"🔐 Login for creator {creator['email']}")

    if res.status_code != 200:
        raise Exception(f"Login failed (HTTP): {res.text}")

    data = res.json()

    if not data.get("success"):
        raise Exception(f"Login failed (API): {data}")

    creator_id = data["data"]["id"]

    token = res.headers.get("token")

    if not token:
        token = data.get("token") or (data.get("data") or {}).get("token")

    if not token:
        raise Exception("Token not found in login response")

    save_token(creator_id, token)

    return token, creator_id


def get_bearer_token(creator):

    if isinstance(creator, int):
        creator_id = creator
        token = get_token(creator_id)

        if token:
            print(f"✅ Using cached token for creator {creator_id}")
            return token

        raise Exception("Token not found in DB and login credentials not provided")

    creator_id = creator.get("id") or creator.get("creator_id")

    if creator_id:
        token = get_token(creator_id)

        if token:
            print(f"✅ Using cached token for creator {creator_id}")
            return token

    print("⚠️ Token not found, logging in...")

    token, creator_id = login_and_save_token(creator)

    creator["id"] = creator_id

    return token