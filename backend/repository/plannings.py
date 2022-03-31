from sqlalchemy.exc import IntegrityError

from backend.db import db_session
from backend.errors import NotFoundError, ConflictError
from backend.models import Planning


class AddPlan:
    name = 'plan'

    def add(self, name: str) -> Planning:
        try:
            new_plan = Planning(name=name)
            db_session.add(new_plan)
            db_session.commit()
        except IntegrityError:
            raise ConflictError(self.name)
        return new_plan

    def get_all(self) -> list[Planning]:
        return Planning.query.all()

    def get_by_id(self, uid: int) -> Planning:
        plan = Planning.query.filter(Planning.uid == uid).first()
        if not plan:
            raise NotFoundError(self.name)
        return plan

    def update(self, uid: int, new_plan: str) -> Planning:
        plan = Planning.query.filter(Planning.uid == uid).first()
        if not plan:
            raise NotFoundError(self.name)
        try:
            plan.name = new_plan
            db_session.commit()
        except IntegrityError:
            raise ConflictError(self.name)
        return plan

    def delete(self, uid: int) -> None:
        plan = Planning.query.filter(Planning.uid == uid).first()
        if not plan:
            raise NotFoundError(self.name)
        db_session.delete(plan)
        db_session.commit()
