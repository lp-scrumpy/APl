from http import HTTPStatus

from backend import schemas
from backend.repository.plannings import PlanningRepo
from flask import Blueprint, request, jsonify

planning = Blueprint('plan', __name__)

add_plan = PlanningRepo()


@planning.post('/')
def new_plan():
    plan_info = request.json
    plan_info = schemas.Plan(**plan_info)

    entity = add_plan.add(plan_info.name, plan_info.date)
    added_plan = schemas.Plan.from_orm(entity)

    return added_plan.dict(), HTTPStatus.CREATED


@planning.get('/')
def get_plans():
    entities = add_plan.get_all()
    plans = [schemas.Plan.from_orm(entity).dict() for entity in entities]
    return jsonify(plans), HTTPStatus.OK
