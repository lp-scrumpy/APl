from http import HTTPStatus

from flask import Blueprint, abort, jsonify, request

from backend import schemas
from backend.repository.estimates import EstimateRepo
from backend.repository.plannings import PlanningRepo
from backend.repository.tasks import TaskRepo
from backend.repository.users import UserRepo

task_view = Blueprint('task', __name__)

plan_repo = PlanningRepo()
task_repo = TaskRepo()
user_repo = UserRepo()
estimate_repo = EstimateRepo()


@task_view.get('/<int:task_id>')
def get_task_by_id(planning_id: int, task_id: int):
    entity = task_repo.get_by_id(task_id)
    task_found = schemas.Task.from_orm(entity)
    return task_found.dict(), HTTPStatus.OK


@task_view.patch('/<int:task_id>')
def set_task_score(planning_id: int, task_id: int):
    payload = request.json
    if not payload:
        abort(400, 'Empty payload')

    score = payload.get('score')
    if not score:
        abort(400, '<Score> field required to patch task')

    entity = task_repo.set_score(
        task_id=task_id,
        score=score,
    )
    patch_task = schemas.Task.from_orm(entity)

    return patch_task.dict(), HTTPStatus.OK


@task_view.post('/<int:task_id>/estimates/')
def add_estimates(planning_id: int, task_id: int):
    estimate_info = request.json
    if not estimate_info:
        abort(400, 'estimate not found')
    estimate_info['uid'] = -1
    estimate_info = schemas.Estimate(**estimate_info)

    entity = estimate_repo.add_estimate(
        estimate_info.user_id,
        estimate_info.storypoint,
        task_id=task_id,
    )
    added_estimate = schemas.Estimate.from_orm(entity)

    return added_estimate.dict(), HTTPStatus.CREATED


@task_view.get('/<int:task_id>/estimates/')
def get_estimates(planning_id: int, task_id: int):
    entities = estimate_repo.get_all_estimates(task_id)
    estimates = [schemas.Estimate.from_orm(entity).dict() for entity in entities]
    return jsonify(estimates), HTTPStatus.OK
