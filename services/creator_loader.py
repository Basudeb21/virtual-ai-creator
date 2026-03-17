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
    behavior = db.fetch_one(behavior_query, (user_id,)) or {}

    persona_query = """
        SELECT tone, speaking_style, interests, most_used_emojis
        FROM ai_creator_persona
        WHERE user_id = %s
    """
    persona = db.fetch_one(persona_query, (user_id,)) or {}

    looks_query = """
        SELECT eye_color, skin_tone, hair_style, hair_color, body_type, breast_size, butt_size
        FROM ai_creator_looks
        WHERE user_id = %s
    """
    looks = db.fetch_one(looks_query, (user_id,)) or {}

    traits_query = """
        SELECT trait_key, trait_value
        FROM ai_creator_traits
        WHERE user_id = %s
    """
    traits_list = db.fetch_all(traits_query, (user_id,)) or []

    traits = {}
    for t in traits_list:
        if not t:
            continue
        key = t.get("trait_key")
        value = t.get("trait_value")
        if key:
            traits[key] = value

    memory_query = """
        SELECT 
            m.fan_id,
            m.summary,
            k.keyword,
            m.importance_score
        FROM ai_creator_memory m
        JOIN keywords k ON m.keyword_id = k.id
        WHERE m.ai_id = %s
        ORDER BY m.importance_score DESC, m.created_at DESC
        LIMIT 50
    """
    memory_list = db.fetch_all(memory_query, (user_id,)) or []

    memory = {}

    for m in memory_list:
        if not m:
            continue

        fan_id = m.get("fan_id")
        if not fan_id:
            continue

        if fan_id not in memory:
            memory[fan_id] = []

        memory[fan_id].append({
            "summary": m.get("summary", ""),
            "tag": m.get("keyword", ""),
            "importance_score": m.get("importance_score", 1)
        })

    creator_data = {
        "user": user,
        "behavior": behavior,
        "persona": persona,
        "looks": looks,
        "traits": traits,
        "memory": memory
    }

    return creator_data