from src.db import database, users
from typing import List


async def fetch_specific_user(user_id: str):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query=query)
