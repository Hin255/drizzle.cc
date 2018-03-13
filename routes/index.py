import os
import uuid
from utils import log
from flask import (
    render_template,
    request,
    redirect,
    session,
    abort,
    url_for,
    Blueprint,
    send_from_directory,
)

from models.topic import Topic
from models.board import Board
from utils import log

from models.user import User
from routes.topic import csrf_tokens
import uuid

main = Blueprint('index', __name__)


def current_user():
    uid = session.get('user_id', -1)
    u = User.find_by(id=uid)
    return u


@main.route("/")
def index():
    return redirect(url_for('topic.index'))


@main.route('/login')
def login():
    return render_template("login.html")


@main.route('/login_dispose', methods=["POST"])
def login_dispose():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        return redirect(url_for('.login'))
    else:
        session['user_id'] = u.id
        session.permanent = True
        return redirect(url_for('topic.index'))


@main.route('/signup')
def signup():
    return render_template("signup.html")


@main.route("/register", methods=["POST"])
def register():
    form = request.form
    u = User.register(form)
    if u is None:
        return redirect(url_for('.signup'))
    else:
        return redirect(url_for('.login'))


@main.route('/signout', methods=['POST'])
def signout():
    u = current_user()
    s = session.get('user_id')
    if s == u.id:
        session.pop('user_id')
        session.pop('_permanent')
        return redirect(url_for('.index'))
    else:
        abort(401)


@main.route("/about")
def about():
    u = current_user()
    return render_template("about.html", user=u)


@main.route("/setting")
def setting():
    u = current_user()
    if u is not None:
        return render_template('setting.html', user=u)
    else:
        return abort(401, "request don't allow")


@main.route("/userinfo_setting", methods=['POST'])
def userinfo_setting():
    u = current_user()
    signature = request.form.get('signature')
    email = request.form.get('email')
    u.signature = signature
    u.email = email
    u.save()
    return render_template('setting.html', user=u)


@main.route("/change_pass", methods=['POST'])
def change_pass():
    u = current_user()
    old_pass = request.form.get('old_pass')
    new_pass = request.form.get('new_pass')
    if u.password == u.salted_password(old_pass):
        s = User.validate_string(new_pass)
        if s:
            u.password = u.salted_password(new_pass)
            u.save()
            return render_template('setting.html', user=u)
        else:
            return abort(401, 'new_password error')
    else:
        return abort(401, 'old_password error')


@main.route('/search', methods=['POST'])
def search():
    value = request.form.get('question', '')
    ts = Topic.all()
    ms = []
    for t in ts:
        if value in t.title:
            ms.append(t)
    return render_template("topic/index.html", ms=ms, )


@main.route('/profile/<user>')
def profile(user):
    u = current_user()
    board_id = int(request.args.get('board_id', -1))
    user = User.find_by(username=user)
    if user is not None:
        ms = Topic.find_all(user_id=user.id)
        token = str(uuid.uuid4())
        csrf_tokens[token] = u.id
        return render_template('profile.html', user=u, ms=ms, otheruser=user, token=token, bid=board_id)
    return abort(401, 'user is None')


def valid_suffix(suffix):
    valid_type = ['jpg', 'png', 'jpeg']
    return suffix in valid_type


@main.route('/image/add', methods=["POST"])
def add_img():
    u = current_user()
    file = request.files['file']
    suffix = file.filename.split('.')[-1]
    if valid_suffix(suffix):
        filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
        file.save(os.path.join('user_image', filename))
        u.user_image = '/uploads/' + filename
        u.save()
    return redirect(url_for('.setting'))


# send_from_directory
# nginx 静态文件
@main.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory('user_image', filename)
