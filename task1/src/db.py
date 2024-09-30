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

    async def replace_or_insert(self, collection_name: str, documents: list[T]):
        """
        Replace existing documents that matches _id and insert the new ones
        """

        collection = self.get_collection(collection_name=collection_name)

        bulk_operation = [
            ReplaceOne({"_id": doc.id}, doc.model_dump(by_alias=True), upsert=True)
            for doc in documents
        ]

        await collection.bulk_write(bulk_operation)

    def close(self):
        self.client.close()


@asynccontextmanager
async def get_db():
    db = MongoDB(db_name=DB_NAME, connection_string=MONGO_DB_CONNECTION_STRING)
    try:
        yield db
    finally:
        db.close()
