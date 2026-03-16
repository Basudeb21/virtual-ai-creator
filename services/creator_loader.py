# services/creator_loader.py
from database.db import db

def load_creator(user_id):
    user_query = """
        SELECT id, username, first_name, last_name, bio, city, state, country_id
        FROM users
        WHERE id = %s
    """
    user = db.fetch_one(user_query, (user_id,))
    
    if not user:
        return None

    behavior_query = """
        SELECT posting_frequency, online_time, offline_time, is_active, current_status,
               personality_prompt, backstory, cooldown_time
        FROM ai_creator_behavior
        WHERE user_id = %s
    """
    behavior = db.fetch_one(behavior_query, (user_id,))

    persona_query = """
        SELECT tone, speaking_style, interests, most_used_emojis
        FROM ai_creator_persona
        WHERE user_id = %s
    """
    persona = db.fetch_one(persona_query, (user_id,))

    looks_query = """
        SELECT eye_color, skin_tone, hair_style, hair_color, body_type, breast_size, butt_size
        FROM ai_creator_looks
        WHERE user_id = %s
    """
    looks = db.fetch_one(looks_query, (user_id,))

    traits_query = """
        SELECT trait_key, trait_value
        FROM ai_creator_traits
        WHERE user_id = %s
    """
    traits_list = db.fetch_all(traits_query, (user_id,))
    traits = {t['trait_key']: t['trait_value'] for t in traits_list}

    memory_query = """
        SELECT fan_user_id, conversation_summary, message
        FROM ai_creator_memory
        WHERE user_id = %s
    """
    memory_list = db.fetch_all(memory_query, (user_id,))
    memory = {m['fan_user_id']: m for m in memory_list}

    creator_data = {
        "user": user,
        "behavior": behavior,
        "persona": persona,
        "looks": looks,
        "traits": traits,
        "memory": memory
    }

    return creator_data