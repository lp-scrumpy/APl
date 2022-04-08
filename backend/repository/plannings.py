from datetime import datetime

from sqlalchemy.exc import IntegrityError

from backend.db import db_session
from backend.errors import ConflictError, NotFoundError
from backend.models import Planning, Task, User, Estimate


class PlanningRepo:
    name = 'plan'

    def add(self, name: str, date: datetime) -> Planning:
        try:
            new_plan = Planning(name=name, date=date)
            db_session.add(new_plan)
            db_session.commit()
        except IntegrityError:
            raise ConflictError(self.name)
        return new_plan

    def get_all(self) -> list[Planning]:
        return Planning.query.all()

    def add_users(self, planning_id: int, name: str) -> User:
        try:
            new_user = User(name=name, planning_id=planning_id)
            db_session.add(new_user)
            db_session.commit()
        except IntegrityError:
            raise ConflictError(self.name)
        return new_user

    def get_all_users(self, planning_id: int) -> list[User]:
        users = User.query.filter(User.planning_id == planning_id)
        return users

    def get_user_by_id(self, planning_id: str, user_id: str) -> User:
        user = User.query.filter(
            User.planning_id == planning_id,
            User.uid == user_id
        ).first()
        if not user:
            raise NotFoundError(self.name)
        return user

    def add_tasks(self, planning_id: int, name: str) -> Task:
        try:
            new_task = Task(name=name, planning_id=planning_id)
            db_session.add(new_task)
            db_session.commit()
        except IntegrityError:
            raise ConflictError(self.name)
        return new_task

    def get_all_tasks(self, planning_id: int) -> list[Task]:
        tasks = Task.query.filter(Task.planning_id == planning_id)
        return tasks

    def get_by_id(self, planning_id: str, task_id: str) -> Task:
        task = Task.query.filter(
            Task.planning_id == planning_id,
            Task.uid == task_id
        ).first()
        if not task:
            raise NotFoundError(self.name)
        return task

    def add_estimate(self, user_id: str, storypoint: str, task_id: int) -> Estimate:
        try:
            new_estimate = Estimate(user_id=user_id, storypoint=storypoint, task_id=task_id)
            db_session.add(new_estimate)
            db_session.commit()
        except IntegrityError:
            raise ConflictError(self.name)
        return new_estimate

    def get_all_estimates(self, task_id: int) -> list[Estimate]:
        estimates = Estimate.query.filter(Estimate.task_id == task_id)
        return estimates
