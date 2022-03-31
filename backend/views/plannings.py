from http import HTTPStatus

from backend import schemas
from backend.repository.plannings import AddPlan
from flask import Blueprint, request, jsonify

planning = Blueprint('plan', __name__)

add_plan = AddPlan()


@planning.get('/')
def get_plans():
    entities = add_plan.get_all()
    plans = [schemas.Plan.from_orm(entity).dict() for entity in entities]
    return jsonify(plans), HTTPStatus.OK


@planning.post('/')
def new_plan():
    plan_info = request.json
    plan_info = schemas.Plan(**plan_info)

    entity = add_plan.add(plan_info.name)
    added_plan = schemas.Plan.from_orm(entity)

    return added_plan.dict(), HTTPStatus.CREATED


@planning.delete('/<uid>')
def delete_plan(uid):
    add_plan.delete(uid)
    return {}, HTTPStatus.NO_CONTENT
