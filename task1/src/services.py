from db import MongoDB


async def get_user_post_count(db: MongoDB, user_id: int):
    return await db.get_collection("posts").count_documents({"user_id": user_id})


async def get_user_activity(db: MongoDB, user_id: int):
    pipeline = user_activity_pipeline()
    pipeline.insert(0, {"$match": {"user_id": user_id}})

    activity = await db.get_collection("posts").aggregate(pipeline).to_list(length=None)

    return (
        activity[0]
        if activity
        else {"user_id": user_id, "post_count": 0, "comment_count": 0}
    )


async def get_all_user_activity(db: MongoDB):
    pipeline = user_activity_pipeline()

    return await db.get_collection("posts").aggregate(pipeline).to_list(length=None)


def user_activity_pipeline():
    return [
        # Join comments on each of the posts
        {
            "$lookup": {
                "from": "comments",
                "localField": "_id",
                "foreignField": "post_id",
                "as": "comments",
            }
        },
        # Group posts by user_id and get sum of posts and also total
        {
            "$group": {
                "_id": "$user_id",
                "post_count": {"$sum": 1},
                "comment_count": {"$sum": {"$size": "$comments"}},
            }
        },
    ]
