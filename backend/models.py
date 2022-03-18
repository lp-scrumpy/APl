from sqlalchemy import Column, Integer, String
from backend.db import Base, engine

class User(Base):
    __tablename__ = 'users'
    uid = Column(Integer, primary_key=True)
    username = Column(String)

    def __repr__(self):
        return f'<User {self.uid} {self.username}>'

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)