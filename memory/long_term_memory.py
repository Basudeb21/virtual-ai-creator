from database.db import get_db_connection

def get_relevant_memories(ai_id: int, fan_id: int, limit: int = 10):
    """
    Load important memories for this AI + user
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT summary
    FROM memory
    WHERE ai_id = %s
      AND fan_id = %s
    ORDER BY importance_score DESC, last_used_at DESC
    LIMIT %s
    """

    cursor.execute(query, (ai_id, fan_id, limit))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [row["summary"] for row in rows]