from typing import TypeVar
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class MongoDB:
    def __init__(self, db_name: str, connection_string: str):
        self.client = AsyncIOMotorClient(connection_string)
        self.db = self.client[db_name]

    def get_collection(self, collection_name: str):
        return self.db[collection_name]

    async def insert_many(self, collection_name: str, documents: list[T]):
        collection = self.get_collection(collection_name=collection_name)
        document_dicts = [document.model_dump() for document in documents]
        await collection.insert_many(document_dicts)

    def close(self):
        self.client.close()
