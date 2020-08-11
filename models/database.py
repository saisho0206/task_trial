from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

DATABASE = 'postgresql'
USER = 'saishodaiki'
PASSWORD = 'dike0206'
HOST = 'localhost'
PORT = '5432'
DB_NAME = 'mydb'
CONNECT_STR = '{}://{}:{}@{}:{}/{}'.format(DATABASE, USER, PASSWORD, HOST, PORT, DB_NAME)
engine = create_engine(CONNECT_STR, convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import models.models
    Base.metadata.create_all(bind=engine)
