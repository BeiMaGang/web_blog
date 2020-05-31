import json

from flask import (
    Blueprint, request)

from dal.Blog import Blog
from dal.Comments import Comment
from dal.Concern import Concern
from dal.User import User
from dal.conf import get_db_session
from util.GenerateID import generate_id
from util.decorator import login_needed
from util.encoder import AlchemyEncoder

bp = Blueprint('blog', __name__, url_prefix='/blog')


@bp.route("/article", methods=["GET"])
@login_needed
def article():
    blog_id = int(request.args.get("blog_id", 0))
    blog_info = get_blogs_info([blog_id]).get(blog_id)
    return json.dumps({
        "status": 200,
        "message": "成功",
        "data": blog_info
    }, ensure_ascii=False)


@bp.route("/get_blogs", methods=["GET"])
@login_needed
def get_blogs():
    type = int(request.args.get("type"))
    blog_id = int(request.args.get("blog_id", 0))
    DBsession = get_db_session()
    user = getattr(request, "user", {})
    blogger_ids = []
    if type == 0:
        blogger_ids.append(user.get("id"))
    elif type == 1:
        if blog_id == 0:
            concerns = DBsession.query(Concern).filter(Concern.user_id == user.get("id")).all()
            for c in concerns:
                blogger_ids.append(c.blogger_id)
        else:
            blogger_ids.append(blog_id)

    if type == 2:
        blogs = DBsession.query(Blog).order_by(Blog.create_time.desc()).all()
    else:
        blogs = DBsession.query(Blog).filter(Blog.user_id.in_(blogger_ids)).order_by(Blog.create_time.desc()).all()

    blog_ids = [blog.id for blog in blogs]

    blog_dic = get_blogs_info(blog_ids)
    return json.dumps({
        "status": 200,
        "message": "成功",
        "data": list(blog_dic.values())
    }, ensure_ascii=False)


@bp.route("/create_blog", methods=["POST"])
@login_needed
def create_blog():
    user = getattr(request, "user", {})
    title = request.form["title"]
    content = request.form["content"]
    new_blog = Blog(
        id=generate_id(),
        user_id=user.get("id"),
        title=title,
        content=content
    )
    DBsession = get_db_session()
    DBsession.add(new_blog)
    DBsession.commit()
    return json.dumps({
        "status": 200,
        "message": "创建成功",
        "data": json.loads(json.dumps(new_blog, cls=AlchemyEncoder))
    }, ensure_ascii=False)


@bp.route("/modify_blog", methods=["POST"])
@login_needed
def modify_blog():
    user = getattr(request, "user", {})
    blog_id = int(request.form["blog_id"])
    title = request.form["title"]
    content = request.form["content"]
    DBsession = get_db_session()
    blog = DBsession.query(Blog).filter(Blog.id == blog_id).first()
    if user.get("id", 0) != blog.user_id:
        return json.dumps({
        "status": 701,
        "message": "您不是此文章的作者无法修改",
    }, ensure_ascii=False)
    blog.title = title
    blog.content = content
    DBsession.commit()

    return json.dumps({
        "status": 200,
        "message": "修改成功",
        "data": json.loads(json.dumps(blog, cls=AlchemyEncoder))
    }, ensure_ascii=False)


def get_blogs_info(blog_ids):
    DBsession = get_db_session()
    blogs = DBsession.query(Blog).filter(Blog.id.in_(blog_ids)).order_by(Blog.create_time.desc()).all()
    blog_dic = {blog.id: json.loads(json.dumps(blog, cls=AlchemyEncoder, ensure_ascii=False)) for blog in blogs}
    user_ids = [blog.user_id for blog in blogs]
    users = DBsession.query(User).filter(User.id.in_(user_ids)).all()
    user_dic = {user.id: user for user in users}
    for blog in blog_dic.values():
        blog["comments"] = []
        blog["author"] = json.loads(json.dumps(user_dic.get(blog["user_id"], {}), cls=AlchemyEncoder, ensure_ascii=False))
    comments = DBsession.query(Comment).filter(Comment.blog_id.in_(blog_dic.keys())).order_by(Comment.create_time.desc()).all()

    for comment in comments:
        comment_user = DBsession.query(User).filter(User.id == comment.user_id).first()
        comment.__setattr__("user", json.loads(json.dumps(comment_user, cls=AlchemyEncoder)))
        blog_dic.get(comment.blog_id).get("comments", []).append(json.loads(json.dumps(comment, cls=AlchemyEncoder)))

    return blog_dic