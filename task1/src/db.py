from contextlib import asynccontextmanager
from typing import TypeVar
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pymongo import ReplaceOne

import os
from dotenv import load_dotenv


load_dotenv()

MONGO_DB_CONNECTION_STRING = os.getenv("MONGO_DB_CONNECTION_STRING")
DB_NAME = os.getenv("DB_NAME")


T = TypeVar("T", bound=BaseModel)


class MongoDB:
    def __init__(self, db_name: str, connection_string: str):
        self.client = AsyncIOMotorClient(connection_string)
        self.db = self.client[db_name]

    def get_collection(self, collection_name: str):
        return self.db[collection_name]

    def close(self):
        self.client.close()


@asynccontextmanager
async def db_context():
    """
    Create an instance of mongo db and ensure that it is closed when exiting the context
    """
    db = MongoDB(db_name=DB_NAME, connection_string=MONGO_DB_CONNECTION_STRING)
    try:
        yield db
    finally:
        db.close()


async def get_db():
    """
    Yield a db instance that can be used with FastAPI Depends().
    """

    async with db_context() as db:
        yield db
