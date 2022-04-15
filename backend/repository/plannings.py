from datetime import datetime

from sqlalchemy.exc import IntegrityError

from backend.db import db_session
from backend.errors import ConflictError, NotFoundError
from backend.models import Planning


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

    def get_by_id(self, planning_id: int) -> Planning:
        entity = Planning.query.get(planning_id)
        if not entity:
            raise NotFoundError('planning')

        return entity
