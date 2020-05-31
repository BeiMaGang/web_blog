# coding = utf8
import json

from flask import (
    Blueprint, request, make_response, Response)

from dal.User import User
from dal.conf import get_db_session
from util.GenerateID import generate_id
from util.decorator import login_needed
from util.encoder import AlchemyEncoder
from util.redis_session import set_session, get_session, delete_session

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['POST'])
def register():
    account = request.form['account']
    passwd = request.form['passwd']
    nick_name = request.form['nick_name']
    session = get_db_session()
    users = session.query(User).filter(User.account == account).first()

    response = make_response('设置cookie')
    response.set_cookie("user_id", "111")
    if users:
        return json.dumps({
            "status": 901,
            "message": "username已经被注册"
        })
    user = User(
        id=generate_id(),
        account=account,
        passwd=passwd,
        nick_name=nick_name,
    )
    session.add(user)
    session.commit()
    return json.dumps({
            "status": 200,
            "message": "注册成功"
        })


@bp.route('/login', methods=['POST'])
def login():
    account = request.form['account']
    passwd = request.form['passwd']
    session = get_db_session()
    user = session.query(User).filter(User.account == account).first()
    if not user:
        return Response(json.dumps({
            "status": 801,
            "message": "username不存在"
        }))
    if passwd != user.passwd:
        return Response(json.dumps({
            "status": 802,
            "message": "账户密码不正确"
        }))
    res = Response(json.dumps({
            "status": 200,
            "message": "登陆成功"
        }))
    session_key = set_session(user)
    res.set_cookie("session_key", session_key)
    return res


@bp.route('/auto_login', methods=["GET"])
def auto_login():
    info = get_session(request.cookies.get("session_key", ""))
    if info:
        return json.dumps({
            "status": 200,
            "message": info.get("nick_name") + "自动登录成功"
        })
    else:
        return json.dumps({
            "status": 801,
            "message": "请登录"
        })


@bp.route('/logout', methods=["GET", 'POST'])
@login_needed
def logout():
    delete_session(request.cookies.get("session_key", ""))
    return json.dumps({
        "status": 200,
        "message": "注销成功"
    })


@bp.route('/test_cookie', methods=['GET'])
@login_needed
def login_process():
    #cookie 等的设置
    response = Response(json.dumps({
            "status": 200,
            "message": "登陆成功",
            "data": json.dumps(request.user)
        }))
    return response