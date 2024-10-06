from datetime import datetime

import uvicorn
from db import MongoDB, get_db
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import TurbineDataResponse

app = FastAPI()

origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/turbine/{turbine_id}", response_model=list[TurbineDataResponse])
async def turbine_data(
    turbine_id: int,
    start_time: datetime | None = None,
    end_time: datetime | None = None,
    db: MongoDB = Depends(get_db),
):
    collection = db.get_collection("turbine_data")
    query = {"turbine_id": turbine_id}

    # Add filter start- and end_time filter if needed
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
