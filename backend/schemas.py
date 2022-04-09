from datetime import datetime
from pydantic import BaseModel, Field


class Schema(BaseModel):

    class Config:
        orm_mode = True


class User(Schema):
    uid: int
    planning_id: int
    name: str


class Plan(Schema):
    uid: int
    name: str = Field(min_length=0, max_length=15)
    date: datetime


class Task(Schema):
    uid: int
    planning_id: int
    name: str


class Estimate(Schema):
    uid: int
    storypoint: int
    user_id: int
    task_id: int
