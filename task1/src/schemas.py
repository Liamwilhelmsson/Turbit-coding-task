from pydantic import AliasChoices, BaseModel, Field


class UserPostCountResponse(BaseModel):
    user_id: int = Field(validation_alias=AliasChoices("_id", "user_id"))
    post_count: int


class UserCommentCountResponse(BaseModel):
    user_id: int = Field(validation_alias=AliasChoices("_id", "user_id"))
    comment_count: int


class UserActivityResponse(BaseModel):
    user_id: int = Field(validation_alias=AliasChoices("_id", "user_id"))
    post_count: int
    comment_count: int
