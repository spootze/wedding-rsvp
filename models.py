from sqlalchemy import Column, Integer, String, DateTime, func
from database import Base

class Registration(Base):
    __tablename__ = 'registration'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    count = Column(Integer)
    created_date = Column(DateTime, server_default=func.now())

    def __init__(self, name=None, email=None, count=1):
        self.name = name
        self.email = email
        self.count = 1

    def __repr__(self):
        return '<User %r>' % (self.name)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    