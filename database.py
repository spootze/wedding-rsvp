from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Database(object):

  def __init__(self, application):
    self.engine = create_engine(application.config['DB_CONNECTION_STRING'],
      convert_unicode=True)

    self.db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=self.engine))

    Base.query = self.db_session.query_property()



  def init_db(self):
      import models
      Base.metadata.create_all(bind=self.engine)
