import orjson
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

    return orjson.dumps(added_plan.dict()), HTTPStatus.CREATED


@planning.get('/')
def get_plans():
    entities = add_plan.get_all()
    plans = [schemas.Plan.from_orm(entity).dict() for entity in entities]
    return jsonify(plans), HTTPStatus.OK


@planning.get('/<planning_id>/tasks/')
def get_tasks(planning_id):
    entities = add_plan.get_all_tasks(planning_id)
    tasks = [schemas.Task.from_orm(entity).dict() for entity in entities]
    return jsonify(tasks), HTTPStatus.OK


@planning.get('/<planning_id>/tasks/<task_id>')
def get_task_by_id(planning_id, task_id):
    entity = add_plan.get_by_id(planning_id, task_id)
    task_found = schemas.Task.from_orm(entity)
    return task_found.dict(), HTTPStatus.OK


@planning.post('/<planning_id>/tasks/')
def add_task(planning_id):
    task_info = request.json
    task_info['uid'] = -1
    task_info = schemas.Task(**task_info)

    entity = add_plan.add_tasks(task_info.planning_id, task_info.name)
    added_task = schemas.Task.from_orm(entity)

    return added_task.dict(), HTTPStatus.CREATED
