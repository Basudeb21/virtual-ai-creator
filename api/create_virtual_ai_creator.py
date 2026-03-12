from fastapi import FastAPI, HTTPException
import requests
import os
import sys
# Add project root to Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
from config.platform_api import API_REGISTER_URL
from database.ai_creator_schema import CreateAICreator
from database.ai_creator_queries import insert_ai_creator_data

app = FastAPI()

@app.post("/create_ai_creator")
def create_ai_creator(ai_creator: CreateAICreator):
    # Step 1: Register the user via the Laravel API
    payload = {
        "utype": ai_creator.utype,
        "referral_code": ai_creator.referral_code,
        "first_name": ai_creator.first_name,
        "last_name": ai_creator.last_name,
        "email": ai_creator.email,
        "password": ai_creator.password,
        "confirm_password": ai_creator.confirm_password,
        "phone": ai_creator.phone,
        "address": ai_creator.address,
        "city": ai_creator.city,
        "state": ai_creator.state,
        "country": ai_creator.country,
        "zipcode": ai_creator.zipcode,
        "ssn": ai_creator.ssn,
        "categories": ai_creator.categories,
        "facebook": ai_creator.facebook,
        "instagram": ai_creator.instagram,
        "tiktok": ai_creator.tiktok,
        "twitter": ai_creator.twitter,
        "youtube": ai_creator.youtube,
        "website": ai_creator.website
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.post(API_REGISTER_URL, json=payload, headers=headers)
    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    result = response.json()

    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result)

    user_data = result["data"]

    # Step 2: Insert AI creator data into the database
    ai_id = insert_ai_creator_data(ai_creator, user_data)

    return {
        "message": "AI creator created",
        "user_id": ai_id,
        "username": user_data["username"],
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.create_virtual_ai_creator:app", host="0.0.0.0", port=8000, reload=True)