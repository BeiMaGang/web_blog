# coding = utf8
import json
from datetime import datetime

from flask import (
    Blueprint, request)

from dal.Comments import Comment
from dal.conf import get_db_session
from util.GenerateID import generate_id
from util.decorator import login_needed
from util.encoder import AlchemyEncoder

bp = Blueprint('comment', __name__, url_prefix='/comment')


@bp.route("/comment_blog", methods=["POST"])
@login_needed
def comment_blog():
    user = getattr(request, "user")
    DBsession = get_db_session()
    blog_id = request.form["blog_id"]
    comment = request.form["comment"]
    one = Comment(
        id=generate_id(),
        user_id=user["id"],
        blog_id=blog_id,
        content=comment,
        create_time=datetime.now(),
    )
    DBsession.add(one)
    setattr(one, "user", user)
    DBsession.commit()
    return json.dumps({
        "status": 200,
        "message": "评论成功",
        "data": json.loads(json.dumps(one, cls=AlchemyEncoder))
    }, ensure_ascii=False)
