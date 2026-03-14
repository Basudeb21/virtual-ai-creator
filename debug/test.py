import requests
import json
from auth.token_manager import get_bearer_token

url = "https://beta-admin.fliqzworld.com/api/post?page=1"

ai_creator = {
    "id": 148,
    "email": "u3114976935",
    "password": "Jesika@2003"
}

def fetch_creator_posts(ai_creator):

    creator_id = ai_creator["id"]

    token = get_bearer_token(ai_creator)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers)

        print("Status Code:", response.status_code)

        if response.status_code != 200:
            print("Error Response:", response.text)
            return []

        data = response.json()
        posts = data["data"]["data"]

        creator_posts = []

        for post in posts:

            # filter only creator's posts
            if post["user"]["id"] != creator_id:
                continue

            post_data = {
                "post_id": post["id"],
                "text": post["text"],
                "comments": []
            }

            if post["comment"]:
                for c in post["comment"]:
                    post_data["comments"].append({
                        "username": c["user"]["username"],
                        "message": c["message"]
                    })

            creator_posts.append(post_data)

        return creator_posts

    except Exception as e:
        print("Request failed:", str(e))
        return []
    


posts = fetch_creator_posts(ai_creator)
print("Checking posts for creator:", ai_creator["id"])
for post in posts:

    print("\n==============================")
    print("Post ID:", post["post_id"])
    print("Post Text:", post["text"])

    for c in post["comments"]:
        print("User:", c["username"])
        print("Message:", c["message"])    