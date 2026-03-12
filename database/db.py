# database/db.py

import mysql.connector
from mysql.connector import pooling

from config.settings import (
    DB_HOST,
    DB_USER,
    DB_PASSWORD,
    DB_NAME,
    DB_POOL_SIZE
)

dbconfig = {
    "host": DB_HOST,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "database": DB_NAME
}

pool = pooling.MySQLConnectionPool(
    pool_name="ai_creator_pool",
    pool_size=DB_POOL_SIZE,
    **dbconfig
)


class DB:

    def get_connection(self):
        return pool.get_connection()

    def fetch_one(self, query, params=None):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(query, params)
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result

    def fetch_all(self, query, params=None):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(query, params)
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        return result

    def execute(self, query, params=None):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(query, params)
        conn.commit()

        cursor.close()
        conn.close()


db = DB()