from pydantic import AliasChoices, BaseModel, Field


class Post(BaseModel):
    id: int
    user_id: int = Field(validation_alias=AliasChoices("user_id", "userId"))
    title: str
    body: str


class Comment(BaseModel):
    id: int
    post_id: int = Field(validation_alias=AliasChoices("post_id", "postId"))
    name: str
    email: str
    body: str
