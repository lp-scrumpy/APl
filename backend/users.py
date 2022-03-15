from http import HTTPStatus
from uuid import uuid4

import werkzeug
from flask import Flask, Blueprint, jsonify, request
from pydantic import ValidationError
from werkzeug.exceptions import BadRequest

from backend.schemas import UserSchema

user = Blueprint('user', __name__)


users_name = {
    "2e23eb29-b203-4092-859f-8cd26ccec909": {
        "uid": "2e23eb29-b203-4092-859f-8cd26ccec909",
        "username": "Миша",
    },
    "229aeb06-ba19-47db-8652-441f1e8eb950": {
        "uid": "2e23eb29-b203-4092-859f-8cd26ccec909",
        "username": "Маша",
    },
}

@user.get('/')
def get_users():
    users = [user for _, user in users_name.items()]
    return jsonify(users)


@user.get('<uid>')
def get_user_id(uid):
    user = users_name.get(uid)
    if not user:
        return {'message':'user not found'}, HTTPStatus.NOT_FOUND

    return user

@user.post('/')
def add_user():
    try:
        user = request.json
        user['uid'] = uuid4().hex
        new_user = UserSchema(**user)
    except ValidationError as e:
        return e.json(), HTTPStatus.BAD_REQUEST
    except werkzeug.exceptions.BadRequest:
        return {"message": "incorrect data"}, HTTPStatus.BAD_REQUEST
    users_name[user['uid']] = user

    return new_user.dict(), HTTPStatus.CREATED

@user.put('<uid>')
def update_user(uid):
    if uid not in users_name:
        return {"message": "user not found"}, HTTPStatus.NOT_FOUND
    try:
        uid = request.json
        new_uid = UserSchema(**uid)
    except ValidationError as e:
        return e.json(), HTTPStatus.BAD_REQUEST
    except werkzeug.exceptions.BadRequest:
         return {'message': 'incorrect data'}, HTTPStatus.BAD_REQUEST

    users_name[uid] = user
    return new_uid.dict(), HTTPStatus.OK

@user.delete('<uid>')
def delete_user(uid):
    if uid not in users_name:
        return {"message":"user not found"}, HTTPStatus.NOT_FOUND
    users_name.pop(uid)
    return {}, HTTPStatus.NO_CONTENT
