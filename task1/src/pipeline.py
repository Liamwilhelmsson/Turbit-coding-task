import asyncio

import os
from dotenv import load_dotenv
from pydantic import BaseModel

from http_client import AsyncHttpClient
from models import Post, Comment
from db import MongoDB, get_db

load_dotenv()

BASE_URL = "https://jsonplaceholder.typicode.com/"


async def fetch_and_store(
    client: AsyncHttpClient,
    db: MongoDB,
    endpoint: str,
    model: BaseModel,
):
    data = await client.get(endpoint=endpoint)
    documents = [model.model_validate(entry) for entry in data]
    await db.replace_or_insert(collection_name=endpoint, documents=documents)


async def main():
    async with get_db() as db:
        async with AsyncHttpClient(base_url=BASE_URL) as client:
            tasks = [
                fetch_and_store(client=client, db=db, endpoint="posts", model=Post),
                fetch_and_store(
                    client=client, db=db, endpoint="comments", model=Comment
                ),
            ]

            await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
