from backend.db import db_session
from backend.models import User


class AddUser:
    name = 'user'

    def add(self, username: str) -> User:
        new_user = User(username=username)
        db_session.add(new_user)
        db_session.commit()
        return new_user

    def get_all(self) -> User:
        return User.query.all()

    def get_by_id(self, uid: int) -> User:
        user = User.query.filter(User.uid == uid).first()
        return user

    def update(self, uid: int, new_name: str) -> User:
        user = User.query.filter(User.uid == uid).first()
        user.username = new_name
        db_session.commit()
        return user 

    def delete(self, uid: int) -> None:
        user = User.query.filter(User.uid == uid).first()
        db_session.delete(user)
        db_session.commit()
        return user



