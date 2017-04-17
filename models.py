from sqlalchemy import Column, ForeignKeyConstraint, Integer, String, DateTime, func
from database import Base

class Registration(Base):
    __tablename__ = 'registration'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    allergies = Column(String(1000))
    program_request = Column(String(1000))
    info = Column(String(1000))
    count = Column(Integer)
    created_date = Column(DateTime, server_default=func.now())

    def __init__(self, name=None, email=None, allergies=None,
      program_request=None, info=None, count=0):

        self.name = name
        self.email = email
        self.allergies = allergies
        self.program_request = program_request
        self.info = info
        self.count = count
        
    def __repr__(self):
        return '<Registration %r>' % (self.name)

class Gift(Base):
  __tablename__ = 'gift'
  id = Column(Integer, primary_key=True)
  title = Column(String(200))
  link = Column(String(200))
  initial_count = Column(Integer)

  def __init__(self, title=None, link=None, initial_count=0):
        self.title = title
        self.link = link
        self.initial_count = initial_count
        self.remaining_count = None

class GiftRegistration(Base):
  __tablename__ = 'gift_registration'
  id = Column(Integer, primary_key=True)
  gift_id = Column(Integer, nullable=False)
  count = Column(Integer)
  created_date = Column(DateTime, server_default=func.now())
  ForeignKeyConstraint(['gift_id'],['gift.id'])

  def __init__(self, gift_id, count):
    self.gift_id = gift_id
    self.count = count

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    