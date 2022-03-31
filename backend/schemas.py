from datetime import datetime
from pydantic import BaseModel, Field


class Schema(BaseModel):

    class Config:
        orm_mode = True


class User(Schema):
    uid: str
    username: str = Field(min_length=1, max_length=15)


class Plan(Schema):
    uid: str
    name: str = Field(min_length=1, max_length=15)
    date: datetime
