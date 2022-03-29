from sqlalchemy import Column, Integer, String, DateTime
from backend.db import Base, engine


class User(Base):
    __tablename__ = 'users'
    uid = Column(Integer, primary_key=True)
    username = Column(String)

    def __repr__(self):
        return f'<User {self.uid} {self.username}>'


class Planning(Base):
    __tablename__ = 'plannings'
    uid = Column(Integer, primary_key=True)
    name = Column(String)
    date = Column(DateTime)

    def __repr__(self):
        return f'<Planning {self.uid} {self.name} {self.date}>'
    

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
