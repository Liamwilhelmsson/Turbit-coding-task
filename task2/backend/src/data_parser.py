import asyncio
import os

import pandas as pd
from db import db_context
from dotenv import load_dotenv
from models import TurbineData
from motor.motor_asyncio import AsyncIOMotorCollection

load_dotenv()

FILEPATH_PER_TURBINE = {
    1: "Turbine1.csv",
    2: "Turbine2.csv",
}  # Could also be fetched directly but out of scope


async def parse_and_store_csv(
    collection: AsyncIOMotorCollection, turbine_id: int, file_path: str
):
    df = pd.read_csv(
        file_path,
        delimiter=";",
        decimal=",",
        skipinitialspace=True,
        skiprows=[1],
    )

    turbine_data = [
        TurbineData(turbine_id=turbine_id, **row) for row in df.to_dict("records")
    ]

    await collection.insert_many(documents=[data.model_dump() for data in turbine_data])


async def main():
    curr_dir = os.path.dirname(__file__)

    tasks = []
    async with db_context() as db:
        collection = db.get_collection(collection_name="turbine_data")
        for turbine_id, file in FILEPATH_PER_TURBINE.items():
            file_path = os.path.join(curr_dir, "..", "data", file)
            tasks.append(
                parse_and_store_csv(
                    collection=collection, turbine_id=turbine_id, file_path=file_path
                )
            )

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
