# coding = utf8
from .conf import Base, Common_column
from sqlalchemy import Column, String, Integer


class Comment(Base, Common_column):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=1)
    user_id = Column(Integer)
    blog_id = Column(Integer)
    content = Column(String)
    status = Column(Integer, default=0)