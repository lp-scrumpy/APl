from http import HTTPStatus

import orjson
from flask import Blueprint, abort, jsonify, request

from backend import schemas
from backend.repository.plannings import PlanningRepo
from backend.repository.tasks import TaskRepo

planning = Blueprint('plan', __name__)

plan_repo = PlanningRepo()
task_repo = TaskRepo()


@planning.post('/')
def new_plan():
    plan_info = request.json
    plan_info = schemas.Plan(**plan_info)

    entity = plan_repo.add(plan_info.name, plan_info.date)
    added_plan = schemas.Plan.from_orm(entity)

    return orjson.dumps(added_plan.dict()), HTTPStatus.CREATED


@planning.get('/')
def get_plans():
    entities = plan_repo.get_all()
    plans = [schemas.Plan.from_orm(entity).dict() for entity in entities]
    return jsonify(plans), HTTPStatus.OK


@planning.get('/<planning_id>/tasks/')
def get_tasks(planning_id):
    entities = plan_repo.get_all_tasks(planning_id)
    tasks = [schemas.Task.from_orm(entity).dict() for entity in entities]
    return jsonify(tasks), HTTPStatus.OK


@planning.get('/<planning_id>/tasks/<task_id>')
def get_task_by_id(planning_id, task_id):
    entity = plan_repo.get_by_id(planning_id, task_id)
    task_found = schemas.Task.from_orm(entity)
    return task_found.dict(), HTTPStatus.OK


@planning.post('/<planning_id>/tasks/')
def add_task(planning_id):
    task_info = request.json
    task_info['uid'] = -1
    task_info = schemas.Task(**task_info)

    entity = plan_repo.add_tasks(task_info.planning_id, task_info.name)
    added_task = schemas.Task.from_orm(entity)

    return added_task.dict(), HTTPStatus.CREATED


@planning.patch('/<int:planning_id>/tasks/<int:task_id>')
def set_task_score(task_id: int, planning_id: int):
    payload = request.json
    if not payload:
        abort(400, 'Empty payload')

    score = payload.get('score')
    if not score:
        abort(400, '<Score> field required to patch task')

    entity = task_repo.set_score(
        task_id=task_id,
        planning_id=planning_id,
        score=score,
    )
    patch_task = schemas.Task.from_orm(entity)

    return patch_task.dict(), HTTPStatus.OK
