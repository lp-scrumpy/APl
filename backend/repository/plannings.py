from datetime import datetime
from sqlalchemy.exc import IntegrityError

from backend.db import db_session
from backend.errors import ConflictError, NotFoundError
from backend.models import Planning, Task


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

    def patch(self, name: str, task_id: str, planning_id: str) -> Task:
        task = Task.query.filter(
            Task.uid == task_id,
            Task.planning_id == planning_id
        ).first()
        if not task:
            raise NotFoundError(self.name)
        try:
            task.name = name
            db_session.commit()
        except IntegrityError:
            raise ConflictError(self.name)

        return task
