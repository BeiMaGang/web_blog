# coding = utf8
from .conf import Base, Common_column
from sqlalchemy import Column, String, Integer


class Blog(Base, Common_column):
    __tablename__ = 'blog'
    id = Column(Integer, primary_key=1)
    user_id = Column(Integer)
    title = Column(String)
    content = Column(String)
    status = Column(Integer, default=1)

