# database/ai_creator_queries.py
import json
from database.db import db


def insert_ai_creator(data, user_data, cursor):

    query = """
    INSERT INTO ai_creator_looks (
        user_id,
        eye_color,
        skin_tone,
        hair_style,
        hair_color,
        body_type,
        breast_size,
        butt_size
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (
        user_data['id'],
        data.eye_color,
        data.skin_tone,
        data.hair_style,
        data.hair_color,
        data.body_type,
        data.breast_size,
        data.butt_size
    ))


def insert_ai_creator_behaviour(data, user_data, cursor):

    query = """
    INSERT INTO ai_creator_behavior (
        user_id,
        posting_frequency,
        online_time,
        offline_time,
        is_active,
        current_status,
        admin_id,
        personality_prompt,
        backstory,
        cooldown_time
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (
        user_data['id'],
        data.posting_frequency,
        data.online_time,
        data.offline_time,
        data.is_active,
        data.current_status,
        data.admin_id,
        data.personality_prompt,
        data.backstory,
        data.cooldown_time
    ))


def insert_ai_creator_persona(data, user_data, cursor):

    query = """
    INSERT INTO ai_creator_persona (
        user_id,
        tone,
        interests,
        speaking_style,
        most_used_emojis
    ) VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(query, (
        user_data['id'],
        data.tone,
        json.dumps(data.interests),
        data.speaking_style,
        json.dumps(data.most_use_emojis)
    ))


def insert_ai_creator_traits(data, user_data, cursor):

    query = """
    INSERT INTO ai_creator_traits (
        user_id,
        trait_key,
        trait_value
    ) VALUES (%s, %s, %s)
    """

    for key, value in data.persona_traits.items():
        cursor.execute(query, (
            user_data['id'],
            key,
            value
        ))


def insert_ai_creator_data(data, user_data):

    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        insert_ai_creator(data, user_data, cursor)
        insert_ai_creator_behaviour(data, user_data, cursor)
        insert_ai_creator_persona(data, user_data, cursor)
        insert_ai_creator_traits(data, user_data, cursor)

        conn.commit()

        print("AI creator data inserted successfully for:", user_data['username'])

        return user_data['id']

    except Exception as e:

        conn.rollback()
        print("Error inserting AI creator:", str(e))
        raise e

    finally:

        cursor.close()
        conn.close()

def insert_memory(ai_id, fan_id, keyword, summary, importance_score):
    conn = db.get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO ai_creator_memory (
        ai_id,
        fan_id,
        keyword,
        summary,
        importance_score
    ) VALUES (%s, %s, %s, %s, %s)
    """

    try:
        cursor.execute(query, (
            ai_id,
            fan_id,
            keyword,
            summary,
            importance_score
        ))

        conn.commit()
        print("✅ Memory inserted:", keyword, summary)

    except Exception as e:
        conn.rollback()
        print("❌ Memory insert failed::", str(e))
        raise e

    finally:
        cursor.close()
        conn.close()