# database/db.py

import mysql.connector
from mysql.connector import pooling
import logging

from config.settings import (
    DB_HOST,
    DB_USER,
    DB_PASSWORD,
    DB_NAME,
    DB_POOL_SIZE
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger("DB")

dbconfig = {
    "host": DB_HOST,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "database": DB_NAME
}

# Create connection pool
try:
    pool = pooling.MySQLConnectionPool(
        pool_name="ai_creator_pool",
        pool_size=DB_POOL_SIZE,
        **dbconfig
    )
    logger.info("✅ MySQL connection pool created successfully")

except Exception as e:
    logger.error(f"❌ Failed to create MySQL pool: {e}")
    raise


class DB:

    def get_connection(self):
        try:
            conn = pool.get_connection()
            logger.info("✅ MySQL connection acquired from pool")
            return conn

        except Exception as e:
            logger.error(f"❌ Error getting DB connection: {e}")
            raise

    def fetch_one(self, query, params=None):
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(query, params)
            result = cursor.fetchone()

            cursor.close()
            conn.close()

            logger.info("📥 fetch_one query executed")

            return result

        except Exception as e:
            logger.error(f"❌ fetch_one error: {e}")
            return None

    def fetch_all(self, query, params=None):
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(query, params)
            result = cursor.fetchall()

            cursor.close()
            conn.close()

            logger.info("📥 fetch_all query executed")

            return result

        except Exception as e:
            logger.error(f"❌ fetch_all error: {e}")
            return []

    def execute(self, query, params=None):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute(query, params)
            conn.commit()

            cursor.close()
            conn.close()

            logger.info("📤 execute query committed")

        except Exception as e:
            logger.error(f"❌ execute error: {e}")


db = DB()