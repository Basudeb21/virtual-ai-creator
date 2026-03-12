from pydantic import BaseModel
from typing import List, Dict


class CreateAICreator(BaseModel):

    # Laravel register fields
    utype: str = "creator"
    referral_code: str = ""

    first_name: str
    last_name: str
    email: str
    password: str
    confirm_password: str

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

    # AI creator body features
    gender: str
    ethnicity: str
    eye_color: str
    skin_tone: str
    hair_style: str
    hair_color: str
    body_type: str
    age: int
    breast_size: str
    butt_size: str

    # AI behaviour
    niche: str
    tone: str

    posting_frequency: Dict
    #active_hours: Dict
    online_time: str
    offline_time: str
    current_status: str
    admin_id: int
    personality_prompt: str
    backstory: str
    cooldown_time: int

    avatar_style: str
    content_themes: List[str]
    personality_prompt: str

    # AI Creator Persona
    tone: str
    interests: List[str]
    speaking_style: str
    most_use_emojis: List[str]
    persona_traits: Dict[str, str] = {}
    created_by_admin: str
    is_active: bool = True