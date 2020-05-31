# coding = utf8
from .conf import Base, Common_column
from sqlalchemy import Column, String, Integer


class Notice(Base, Common_column):
    __tablename__ = 'notice'
    id = Column(Integer, primary_key=1)
    user_id = Column(Integer)
    content = Column(String)