from http import HTTPStatus

from backend import schemas
from backend.repository.users import AddUser
from flask import Blueprint, jsonify, request
from backend.schemas import UserSchema

user = Blueprint('user', __name__)

add_user = AddUser()

@user.get('/')
def get_users():
    py_models = add_user.get_all()
    users = [schemas.UserSchema.from_orm(py_model).dict() for py_model in py_models]
    return jsonify(users), HTTPStatus.OK


@user.get('<uid>')
def get_user_id(uid):
    py_model = add_user.get_by_id(uid)
    user_found = schemas.UserSchema.from_orm(py_model)
    return user_found.dict(), HTTPStatus.OK

@user.post('/')
def add_users():
    user_info = request.json
    user_info = schemas.UserSchema(**user_info)

    py_model = add_user.add(user_info.username)
    added_user = schemas.UserSchema.from_orm(py_model)

    return added_user.dict(), HTTPStatus.CREATED

@user.put('<uid>')
def update_user(uid):
    user_info = request.json
    user_info = schemas.UserSchema(**user_info)

    py_model = add_user.update(uid, user_info.username)
    update_user = schemas.UserSchema.from_orm(py_model)

    return update_user.dict(), HTTPStatus.OK

@user.delete('<uid>')
def delete_user(uid):
    add_user.delete(uid)
    return {}, HTTPStatus.NO_CONTENT
