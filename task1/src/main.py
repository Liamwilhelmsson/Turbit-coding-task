from fastapi import FastAPI, Depends
import uvicorn

from db import get_db

app = FastAPI()


@app.get("/users/{user_id}/posts/count")
async def user_post_count(user_id: int, db=Depends(get_db)):
    pass


@app.get("/users/{user_id}/comments/count")
async def user_comment_count(user_id: int, db=Depends(get_db)):
    pass


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
