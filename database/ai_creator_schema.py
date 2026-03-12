from pydantic import BaseModel
from typing import List, Dict
from datetime import date,time


class CreateAICreator(BaseModel):

    # Laravel register fields
    utype: str = "creator"
    referral_code: str = ""

    first_name: str
    last_name: str
    email: str
    password: str
    confirm_password: str
    birthdate: date
    gender: str

    phone: str
    address: str
    city: str
    state: str
    country: str
    zipcode: str
    ssn: str
    categories: int

    facebook: str = ""
    instagram: str = ""
    tiktok: str = ""
    twitter: str = ""
    youtube: str = ""
    website: str = ""

    # AI creators 
    
    eye_color: str
    skin_tone: str
    hair_style: str
    hair_color: str
    body_type: str
    breast_size: str
    butt_size: str

    # AI creator behaviour
    posting_frequency: int
    #active_hours: Dict
    online_time: time
    offline_time: time
    is_active: bool = True
    current_status: str
    admin_id: int
    personality_prompt: str
    backstory: str
    cooldown_time: int

    # AI Creator Persona
    tone: str
    interests: List[str]
    speaking_style: str
    most_use_emojis: List[str]


    persona_traits: Dict[str, str] = {}