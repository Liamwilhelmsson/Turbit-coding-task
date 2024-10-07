import asyncio

from db import db_context
from dotenv import load_dotenv
from http_client import AsyncHttpClient
from models import Comment, Post
from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import BaseModel
from pymongo import ReplaceOne

load_dotenv()

BASE_URL = "https://jsonplaceholder.typicode.com/"


async def fetch_and_store(
    client: AsyncHttpClient,
    collection: AsyncIOMotorCollection,
    endpoint: str,
    model: BaseModel,
):
    data = await client.get(endpoint=endpoint)
    documents = [model.model_validate(entry) for entry in data]

    bulk_operation = [
        ReplaceOne({"_id": doc.id}, doc.model_dump(by_alias=True), upsert=True)
        for doc in documents
    ]

    await collection.bulk_write(bulk_operation)


async def main():
    async with db_context() as db:
        async with AsyncHttpClient(base_url=BASE_URL) as client:
            tasks = [
                fetch_and_store(
                    client=client,
                    collection=db.get_collection("posts"),
                    endpoint="posts",
                    model=Post,
                ),
                fetch_and_store(
                    client=client,
                    collection=db.get_collection("comments"),
                    endpoint="comments",
                    model=Comment,
                ),
            ]

            await asyncio.gather(*tasks)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
