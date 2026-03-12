# test_db.py
from database.db import db

users = db.fetch_all("SELECT id, username FROM users LIMIT 5")

print(users)