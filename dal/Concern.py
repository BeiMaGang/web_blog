# coding = utf8
from .conf import Base, Common_column
from sqlalchemy import Column, Integer


class Concern(Base, Common_column):
    __tablename__ = 'concern'
    user_id = Column(Integer, primary_key=1)
    blogger_id = Column(Integer, primary_key=1)