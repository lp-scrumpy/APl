from sqlalchemy import Column, Integer, String, DateTime, Date, Table, ForeignKey
from backend.db import Base, engine
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    uid = Column(Integer, primary_key=True)
    estimate_uid = Column(Integer, ForeignKey('estimates.uid'))
    username = Column(String)
    children = relationship("Planning")
    def __repr__(self):
        return f'<User {self.uid} {self.username} {self.estimate_id}>'


class Planning(Base):
    __tablename__ = 'plannings'
    uid = Column(Integer, primary_key=True)
#    task_uid = Column(Integer, ForeignKey('task.id'))
#    user_uid = Column(Integer, ForeignKey('user.id'))
    name = Column(String)
    date = Column(DateTime)
def __repr__(self):
        return f'<Planning {self.uid} {self.name} {self.date}>'


class Estimate(Base):
    __tablename__ = 'estimates'
    uid = Column(Integer, primary_key=True)
    meaning = Column(String, primary_key=True)
    children = relationship("Task")
    children = relationship("User")
def __repr__(self):
        return f'<Estimate {self.uid} {self.meaning}>'


class Task(Base):
    __tablename__ = 'tasks'
    uid = Column(Integer, primary_key=True)
#    estimate_uid = Column(Integer, ForeignKey('estimate.id'))
    taskname = Column(String)
    children = relationship("Planning")
def __repr__(self):
        return f'<Task {self.uid} {self.estimate_id} {self.taskname}>'


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
