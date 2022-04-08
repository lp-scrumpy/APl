from sqlalchemy.exc import IntegrityError

from backend.db import db_session
from backend.errors import ConflictError, NotFoundError
from backend.models import Task


class TaskRepo:
    name = 'tasks'

    def set_score(self, task_id: int, planning_id: int, score: int) -> Task:
        task = Task.query.filter(
            Task.uid == task_id,
            Task.planning_id == planning_id
        ).first()

        if not task:
            raise NotFoundError(self.name)

        try:
            task.score = score
            db_session.commit()
        except IntegrityError:
            raise ConflictError(self.name)

        return task

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

    def get_by_id(self, planning_id: int, task_id: int) -> Task:
        task = Task.query.filter(
            Task.planning_id == planning_id,
            Task.uid == task_id
        ).first()
        if not task:
            raise NotFoundError(self.name)
        return task
