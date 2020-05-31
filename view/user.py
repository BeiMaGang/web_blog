# coding = utf8
import json

from flask import (
    Blueprint, request)

from dal.Concern import Concern
from dal.User import User
from dal.conf import get_db_session
from util.decorator import login_needed
from util.encoder import AlchemyEncoder

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route("/get_user_info", methods=["GET"])
@login_needed
def get_user_info():
    user = getattr(request, "user")
    user["concerns"] = []
    DBsession = get_db_session()
    concerns = DBsession.query(Concern).filter(Concern.user_id == user.get("id")).all()
    concern_user_ids = [c.blogger_id for c in concerns]
    concern_users = DBsession.query(User).filter(User.id.in_(concern_user_ids)).all()
    for c in concern_users:
        user.get("concerns",[]).append(json.loads(json.dumps(c, cls=AlchemyEncoder)))

    return json.dumps({
            "status": 200,
            "message": "成功",
            "data": user
        })


@bp.route("/concern_one", methods=["POST"])
@login_needed
def concern_one():
    blogger_id = request.form["blogger_id"]
    user = getattr(request, "user")
    DBsession = get_db_session()
    result = DBsession.query(Concern).filter(Concern.user_id == user["id"], Concern.blogger_id == blogger_id).first()
    if result:
        return json.dumps(
            {
                "status": 200,
                "message": "已经关注过此人"
            },
            ensure_ascii=False
        )

    concern = Concern(
        user_id=user["id"],
        blogger_id=blogger_id
    )
    DBsession.add(concern)
    DBsession.commit()
    return json.dumps(
        {
            "status": 200,
            "message": "关注成功"
        },
        ensure_ascii=False
    )
