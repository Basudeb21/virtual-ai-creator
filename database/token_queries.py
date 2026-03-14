# database/token_queries.py

from database.db import db


def save_token(creator_id, token):

    conn = db.get_connection()
    cursor = conn.cursor(buffered=True)

    try:
        query = """
        INSERT INTO ai_creator_sessions (creator_id, token, created_at)
        VALUES (%s, %s, NOW())
        ON DUPLICATE KEY UPDATE token = VALUES(token)
        """

        cursor.execute(query, (creator_id, token))
        conn.commit()

    finally:
        cursor.close()
        conn.close()


def get_token(creator_id):

    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    try:
        query = "SELECT token FROM ai_creator_sessions WHERE creator_id = %s"

        cursor.execute(query, (creator_id,))
        row = cursor.fetchone()

        if row:
            return row["token"]

        return None

    finally:
        cursor.close()
        conn.close()


# if __name__ == "__main__":
#     creator_id = 152
#     token = "example_token_123"

#     save_token(creator_id, token)

#     retrieved_token = get_token(creator_id)

#     print(f"Retrieved token for creator {creator_id}: {retrieved_token}")