# coding = utf8
import json

import functools
from flask import request, redirect, url_for

from util.redis_session import get_session


def login_needed(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        info = get_session(request.cookies.get("session_key", ""))
        if info:
            request.__setattr__("user", info)
            return func(*args, **kw)
        else:
            return json.dumps({
                "status": 302,
                "message": "请登录",
                "url": url_for("index"),
            })
    return wrapper