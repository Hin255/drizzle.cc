from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
)
from utils import log
from routes import *

from models.board import Board


main = Blueprint('board', __name__)


@main.route("/admin")
def index():
    u = current_user()
    if u.id == -2:
        log('111111111111')
        return render_template('board/admin_index.html')
    else:
        return abort(401)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    m = Board.new(form)
    return redirect(url_for('topic.index'))

