from fastapi import FastAPI, Depends
import uvicorn

from db import MongoDB, get_db
from services import get_all_user_activity, get_user_activity

app = FastAPI()


@app.get("/users/{user_id}/posts/count")
async def user_post_count(user_id: int, db: MongoDB = Depends(get_db)):
    """
    Get number of posts for a single user
    """
    post_count = await db.get_collection("posts").count_documents({"user_id": user_id})
    return {"user_id": user_id, "post_count": post_count}


@app.get("/users/{user_id}/comments/count")
async def user_comment_count(user_id: int, db: MongoDB = Depends(get_db)):
    """
    Get number of comments for a single user
    """

    posts = (
        await db.get_collection("posts").find({"user_id": user_id}).to_list(length=None)
    )
    post_ids = [post["_id"] for post in posts]

    comment_count = await db.get_collection("comments").count_documents(
        {"post_id": {"$in": post_ids}}
    )

    return {
        "user_id": user_id,
        "comment_count": comment_count,
    }


@app.get("/users/{user_id}/activity")
async def user_activity(user_id: int, db: MongoDB = Depends(get_db)):

    activity = await get_user_activity(db=db, user_id=user_id)

    return activity


@app.get("/users/activity")
async def all_user_activity(db: MongoDB = Depends(get_db)):

    activity = await get_all_user_activity(db=db)

    return activity


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
