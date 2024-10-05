from datetime import datetime
from fastapi import FastAPI, Depends
import uvicorn

from db import MongoDB, get_db
from schemas import TurbineDataResponse

app = FastAPI()


@app.get("/turbine/{turbine_id}", response_model=list[TurbineDataResponse])
async def turbine_data(
    turbine_id: int,
    start_time: datetime | None = None,
    end_time: datetime | None = None,
    db: MongoDB = Depends(get_db),
):
    collection = db.get_collection("turbine_data")
    query = {"turbine_id": turbine_id}

    if start_time or end_time:
        timestamp_filter = {}
        if start_time:
            timestamp_filter["$gte"] = start_time
        if end_time:
            timestamp_filter["$lte"] = end_time
        query["timestamp"] = timestamp_filter

    data = await collection.find(query).to_list()

    return data


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
