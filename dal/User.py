# coding = utf8
from .conf import Base, Common_column
from sqlalchemy import Column, String, Integer


class User(Base, Common_column):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=1)
    account = Column(String)
    passwd = Column(String)
    nick_name = Column(String)
    gender = Column(String, default='男')
    type = Column(Integer, default=0)