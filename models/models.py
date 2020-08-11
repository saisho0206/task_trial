from sqlalchemy import Column, Integer, String, Text, DateTime
from models.database import Base
from datetime import datetime


class TaskContent(Base):
    __tablename__ = 'taskcontents'
    user_Name = Column(String(128))
    id = Column(Integer, primary_key=True)
    title = Column(String(128), unique=True)
    register_date = Column(DateTime, default=datetime.now())
    update_date = Column(DateTime, default=datetime.now())
    status = Column(Text)
    free = Column(Text)

    def __init__(self, user_Name=None, title=None, registar_date=None,
                    update_date=None, status=None, free=None):
        self.user_Name = user_Name
        self.title = title
        self.registar_date = registar_date
        self.update_date = update_date
        self.status = status
        self.free = free

    def __repr__(self):
        return '<Title %r>' % (self.title)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_name = Column(String(128), unique=True)
    hashed_password = Column(String(128))

    def __init__(self, user_name=None, hashed_password=None):
        self.user_name = user_name
        self.hashed_password = hashed_password

    def __repr__(self):
        return '<Name %r>' % (self.user_name)
