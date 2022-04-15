from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Schema(BaseModel):

    class Config:
        orm_mode = True


class User(Schema):
    uid: int
    name: str


class Plan(Schema):
    uid: int
    name: str = Field(min_length=0, max_length=15)
    date: datetime


class Task(Schema):
    uid: int
    name: str
    score: Optional[int]


class Estimate(Schema):
    uid: int
    user_id: int
    storypoint: Optional[int]
