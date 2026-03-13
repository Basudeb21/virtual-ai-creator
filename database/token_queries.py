from database.db import get_db_connection
import pymysql


def save_token(creator_id, token):

    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    query = """
    INSERT INTO api_tokens (creator_id, token)
    VALUES (%s, %s)
    ON DUPLICATE KEY UPDATE token = VALUES(token)
    """

    cursor.execute(query, (creator_id, token))
    conn.commit()

    cursor.close()
    conn.close()


def get_token(creator_id):

    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    query = "SELECT token FROM api_tokens WHERE creator_id = %s"

    cursor.execute(query, (creator_id,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row:
        return row["token"]

    return None