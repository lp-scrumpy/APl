from sqlalchemy.exc import IntegrityError

from backend.db import db_session
from backend.errors import ConflictError
from backend.models import Estimate


class EstimateRepo:
    name = 'estimates'

    def add_estimate(self, user_id: int, storypoint: int, task_id: int) -> Estimate:
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
