# coding=utf8
import json

from conf import redis_client
import hashlib

from util.GenerateID import generate_id
from util.encoder import AlchemyEncoder


def set_session(user):
    key = hashlib.md5(str(generate_id()).encode(encoding='UTF-8')).hexdigest()
    redis_client.set(key, json.dumps(user, cls=AlchemyEncoder))
    redis_client.expire(key, 10 * 60)
    return key


def get_session(key):
    info = redis_client.get(key)
    if info:
        return json.loads(info.decode('utf8'))
    return info


def delete_session(key):
    redis_client.delete(key)
