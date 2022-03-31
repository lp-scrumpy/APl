from http import HTTPStatus

from backend import schemas
from backend.repository.users import AddUser
from flask import Blueprint, jsonify, request

user = Blueprint('user', __name__)

add_user = AddUser()


@user.get('/')
def get_users():
    entities = add_user.get_all()
    users = [schemas.User.from_orm(entity).dict() for entity in entities]
    return jsonify(users), HTTPStatus.OK


@user.get('/<uid>')
def get_user_id(uid):
    entity = add_user.get_by_id(uid)
    user_found = schemas.User.from_orm(entity)
    return user_found.dict(), HTTPStatus.OK


@user.post('/')
def add_users():
    user_info = request.json
    user_info = schemas.User(**user_info)

    entity = add_user.add(user_info.username)
    added_user = schemas.User.from_orm(entity)

    return added_user.dict(), HTTPStatus.CREATED


@user.put('/<uid>')
def update_user(uid):
    user_info = request.json
    user_info = schemas.User(**user_info)

    entity = add_user.update(uid, user_info.username)
    update_user = schemas.User.from_orm(entity)

    return update_user.dict(), HTTPStatus.OK


@user.delete('/<uid>')
def delete_user(uid):
    add_user.delete(uid)
    return {}, HTTPStatus.NO_CONTENT
