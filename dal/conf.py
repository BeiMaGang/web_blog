# coding = utf8
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from conf import DATABASE_USER, DATABASE_PASSWD

engine = create_engine('mysql+pymysql://{}:{}@120.26.178.240:3306/blog'.format(DATABASE_USER, DATABASE_PASSWD))
Session = sessionmaker(bind=engine)
session = scoped_session(Session)
Base = declarative_base()


def get_db_session():
    return scoped_session(Session)


class Common_column:
    deleted = Column(Integer, default=0)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now)