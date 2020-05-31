# coding = utf8
from datetime import datetime


def generate_id():
    return int(datetime.now().timestamp() * 1000)