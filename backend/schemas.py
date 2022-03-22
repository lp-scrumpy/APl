from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    uid: str
    username: str = Field(min_length=1, max_length=15)

    class Config:
        orm_mode = True
