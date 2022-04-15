from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String,
                        UniqueConstraint)
from sqlalchemy.orm import relationship

from backend.db import Base, engine


class Estimate(Base):
    __tablename__ = 'estimates'
    uid = Column(Integer, primary_key=True)
    storypoint = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('users.uid'))
    task_id = Column(Integer, ForeignKey('tasks.uid'))

    __tableargs__ = (
        UniqueConstraint(task_id, user_id),
    )

    def __repr__(self):
        return f'<Estimate {self.uid} {self.meaning} {self.user_id} {self.task_id}>'


class User(Base):
    __tablename__ = 'users'
    uid = Column(Integer, primary_key=True)
    planning_id = Column(Integer, ForeignKey('plannings.uid'))
    name = Column(String)
    children = relationship("Estimate")

    __table_args__ = (
        UniqueConstraint(name, planning_id),
    )

    def __repr__(self):
        return f'<User {self.uid} {self.planning_id} {self.user_name}>'


class Task(Base):
    __tablename__ = 'tasks'
    uid = Column(Integer, primary_key=True)
    planning_id = Column(Integer, ForeignKey('plannings.uid'))
    name = Column(String)
    score = Column(Integer)

    def __repr__(self):
        return f'<Task {self.uid} {self.planning_id} {self.task_name} {self.score}>'


class Planning(Base):
    __tablename__ = 'plannings'
    uid = Column(Integer, primary_key=True)
    name = Column(String)
    date = Column(DateTime)
    children = relationship('Task')
    children = relationship('User')

    def __repr__(self):
        return f'<Planning {self.uid} {self.name} {self.date}>'


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
