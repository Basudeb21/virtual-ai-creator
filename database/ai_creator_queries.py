import uuid
from database.database_connection import get_db_connection
import pymysql
import json

# Function to insert AI creator data into the database
def insert_ai_creator(data, user_data):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)


    querry = """
    INSERT INTO ai_creators (
        user_id,
        ethnicity,
        age,
        eye_color,
        skin_tone,
        hair_style,
        hair_color,
        body_type,
        breast_size,
        butt_size

    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)    
"""
    cursor.execute(querry, (
        user_data['id'],
        data.ethnicity,
        data.age,
        data.eye_color,
        data.skin_tone,
        data.hair_style,
        data.hair_color,
        data.body_type,
        data.breast_size,
        data.butt_size
    ))

    conn.commit()
    cursor.close()
    conn.close()



def insert_ai_creator_behaviour(data, user_data):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)


    querry = """
    INSERT INTO ai_creator_behavior (
        user_id,
        tone,
        posting_frequency,
        online_time,
        offline_time,
        is_active,
        current_status,
        admin_id,
        personality_prompt,
        backstory,
        cooldown_time
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)    
"""
    cursor.execute(querry, (
        user_data['id'],
        data.tone,
        json.dumps(data.posting_frequency),
        data.online_time,
        data.offline_time,
        data.is_active,
        data.current_status,
        data.admin_id,
        data.personality_prompt,
        data.backstory,
        data.cooldown_time
    ))

    conn.commit()
    cursor.close()
    conn.close()




def insert_ai_creator_persona(data, user_data):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)


    querry = """
    INSERT INTO ai_creator_persona (
        user_id,
        tone,
        interests,
        speaking_style,
        most_use_emojis
    ) VALUES (%s, %s, %s, %s, %s)    
"""
    cursor.execute(querry, (
        user_data['id'],
        data.tone,
        json.dumps(data.interests),
        data.speaking_style,
        json.dumps(data.most_use_emojis)
    ))

    conn.commit()
    cursor.close()
    conn.close()



def insert_ai_creator_traits(data,user_data):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)


    querry = """
    INSERT INTO ai_creator_traits (
        user_id,
       trait_key,
       trait_value
    ) VALUES (%s, %s, %s)    
"""
    for key, value in data.persona_traits.items():
        cursor.execute(querry, (
            user_data['id'],
            key,
            value
        ))

    conn.commit()
    cursor.close()
    conn.close()


def insert_ai_creator_data(data, user_data):
    insert_ai_creator(data, user_data)
    insert_ai_creator_behaviour(data, user_data)
    insert_ai_creator_persona(data, user_data)
    insert_ai_creator_traits(data, user_data)
    print("AI creator data inserted successfully for :", user_data['username'])
    return user_data['id']