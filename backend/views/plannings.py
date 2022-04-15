from http import HTTPStatus

import orjson
from flask import Blueprint, abort, jsonify, request

from backend import schemas
from backend.repository.estimates import EstimateRepo
from backend.repository.plannings import PlanningRepo
from backend.repository.tasks import TaskRepo
from backend.repository.users import UserRepo
from backend.views.tasks import task_view

planning = Blueprint('plan', __name__)
planning.register_blueprint(task_view, url_prefix='/<int:planning_id>/tasks')

plan_repo = PlanningRepo()
task_repo = TaskRepo()
user_repo = UserRepo()
estimate_repo = EstimateRepo()


@planning.post('/')
def new_plan():
    plan_info = request.json
    plan_info['uid'] = -1
    plan_info = schemas.Plan(**plan_info)

    entity = plan_repo.add(plan_info.name, plan_info.date)
    added_plan = schemas.Plan.from_orm(entity)

    return orjson.dumps(added_plan.dict()), HTTPStatus.CREATED


@planning.get('/<int:planning_id>')
def get_by_id(planning_id: int):
    entity = plan_repo.get_by_id(planning_id)
    plan = schemas.Plan.from_orm(entity)

    return orjson.dumps(plan.dict()), HTTPStatus.OK


@planning.get('/')
def get_plans():
    entities = plan_repo.get_all()
    plans = [schemas.Plan.from_orm(entity).dict() for entity in entities]
    return jsonify(plans), HTTPStatus.OK


@planning.post('/<int:planning_id>/users/')
def add_user(planning_id: int):
    task_info = request.json
    if not task_info:
        abort(HTTPStatus.BAD_REQUEST, 'task info required')
    task_info['uid'] = -1
    task_info = schemas.User(**task_info)

    entity = user_repo.add_users(
        planning_id=planning_id,
        name=task_info.name,
    )
    added_user = schemas.User.from_orm(entity)

    return added_user.dict(), HTTPStatus.CREATED


@planning.get('/<planning_id>/users/')
def get_users(planning_id):
    entities = user_repo.get_all_users(planning_id)
    users = [schemas.User.from_orm(entity).dict() for entity in entities]
    return jsonify(users), HTTPStatus.OK


@planning.get('/<planning_id>/users/<user_id>')
def get_user_id(planning_id, user_id):
    entity = user_repo.get_user_by_id(planning_id, user_id)
    user_found = schemas.User.from_orm(entity)
    return user_found.dict(), HTTPStatus.OK


@planning.get('/<planning_id>/tasks/')
def get_tasks(planning_id):
    entities = task_repo.get_all_tasks(planning_id)
    tasks = [schemas.Task.from_orm(entity).dict() for entity in entities]
    return jsonify(tasks), HTTPStatus.OK


@planning.post('/<int:planning_id>/tasks/')
def add_task(planning_id: int):
    task_info = request.json
    if not task_info:
        abort(HTTPStatus.BAD_REQUEST, 'task info required')

    task_info['uid'] = -1
    task_info = schemas.Task(**task_info)

    entity = task_repo.add_tasks(
        planning_id,
        task_info.name
    )
    added_task = schemas.Task.from_orm(entity)

    return added_task.dict(), HTTPStatus.CREATED
