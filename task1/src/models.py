from pydantic import AliasChoices, BaseModel, Field


class Post(BaseModel):
    id: int = Field(alias="_id", validation_alias=AliasChoices("id"))
    user_id: int = Field(validation_alias=AliasChoices("userId"))
    title: str
    body: str


class Comment(BaseModel):
    id: int = Field(alias="_id", validation_alias=AliasChoices("id"))
    post_id: int = Field(validation_alias=AliasChoices("postId"))
    name: str
    email: str
    body: str
