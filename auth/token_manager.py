import requests
from config import API_LOGIN_URL
from database.token_queries import save_token, get_token


#TODO: DB functions for saving and retrieving tokens, with expiration handling

def login_and_save_token(creator):

    res = requests.post(API_LOGIN_URL, json={
        "email_username": creator["email"],
        "password": creator["password"]
    })

    print(f"🔐 Login for creator {creator['id']}")

    if res.status_code != 200:
        raise Exception(f"Login failed (HTTP): {res.text}")

    data = res.json()

    if not data.get("success"):
        raise Exception(f"Login failed (API): {data}")

    token = res.headers.get("token")

    if not token:
        token = data.get("token") or (data.get("data") or {}).get("token")

    if not token:
        raise Exception("Token not found in login response")

    # save token in DB
    # save_token(creator["id"], token)

    return token


def get_bearer_token(creator):

    # token = get_token(creator["id"])
    token = None

    if token:
        return token

    # if token not found, login
    return login_and_save_token(creator)