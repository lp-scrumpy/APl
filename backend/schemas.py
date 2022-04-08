from datetime import datetime
from pydantic import BaseModel, Field


class Schema(BaseModel):

    class Config:
        orm_mode = True


class User(Schema):
    uid: str
    planning_id: str
    name: str


class Plan(Schema):
    uid: str
    name: str = Field(min_length=0, max_length=15)
    date: datetime


class Task(Schema):
    uid: str
    planning_id: str
    name: str


class Estimate(Schema):
    uid: str
    storypoint: str
    user_id: str
    task_id: str
