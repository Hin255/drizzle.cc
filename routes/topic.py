from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
)

from routes import *
from models.topic import Topic
from models.reply import Reply
from models.board import Board
from utils import log


main = Blueprint('topic', __name__)

import uuid

csrf_tokens = dict()


@main.route("/")
def index():
    # board_id = 2
    u = current_user()
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.find_all(board_id=board_id)
    bs = Board.all()
    return render_template("topic/index.html", user=u, ms=ms, bs=bs, bid=board_id, )


@main.route('/<int:id>')
def detail(id):
    u = current_user()
    m = Topic.get(id)
    dt = m.time()
    return render_template("topic/detail.html", user=u, topic=m, time=dt)


@main.route("/add", methods=["POST"])
def add():
    u = current_user()
    form = request.form
    bid = form.get('board_id')
    b = Board.find(int(bid))
    if b is not None and u is not None:
        m = Topic.new(form, user_id=u.id)
        u.topic_amount += 1
        u.save()
        return redirect(url_for('.detail', id=m.id))
    else:
        return abort(401, 'board is error')


@main.route("/delete")
def delete():
    id = int(request.args.get('id'))
    token = request.args.get('token')
    u = current_user()
    if token in csrf_tokens and csrf_tokens[token] == u.id:
        csrf_tokens.pop(token)
        if u is not None:
            print('删除 topic 用户是', u, id)
            replies = Reply.all()
            for r in replies:
                if r.topic_id == id:
                    Reply.delete(r.id)
            Topic.delete(id)
            u.topic_amount -= 1
            u.save()
            return redirect(url_for('.index'))
        else:
            abort(404)
    else:
        abort(403)


def new_csrf_token():
    u = current_user()
    token = str(uuid.uuid4())
    log('token', token)
    csrf_tokens[token] = u.id
    return token


@main.route("/new/<id>")
def new(id):
    u = current_user()
    if u is not None:
        board_id = int(id)
        token = new_csrf_token()
        bs = Board.all()
        return render_template("topic/new.html", user=u, bs=bs, token=token, bid=board_id)
    else:
        return abort(401)
