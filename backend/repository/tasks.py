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
