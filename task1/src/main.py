from fastapi import FastAPI, Depends
import uvicorn

from db import MongoDB, get_db
from services import get_all_user_activity, get_user_activity, get_user_post_count
from schemas import (
    UserActivityResponse,
    UserCommentCountResponse,
    UserPostCountResponse,
)

app = FastAPI()


@app.get("/users/{user_id}/posts/count", response_model=UserPostCountResponse)
async def user_post_count(user_id: int, db: MongoDB = Depends(get_db)):
    count = await get_user_post_count(db, user_id)
    return UserPostCountResponse(user_id=user_id, post_count=count)


@app.get("/users/{user_id}/comments/count", response_model=UserCommentCountResponse)
async def user_comment_count(user_id: int, db: MongoDB = Depends(get_db)):
    return await get_user_activity(db=db, user_id=user_id)


@app.get("/users/{user_id}/activity", response_model=UserActivityResponse)
async def user_activity(user_id: int, db: MongoDB = Depends(get_db)):
    return await get_user_activity(db=db, user_id=user_id)


@app.get("/users/activity", response_model=list[UserActivityResponse])
async def all_user_activity(db: MongoDB = Depends(get_db)):
    return await get_all_user_activity(db=db)


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
