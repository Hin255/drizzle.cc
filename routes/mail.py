from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
)

from routes import *
from models.mail import Mail
from utils import log

main = Blueprint('mail', __name__)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    addressee = form.get('addressee')
    linkman = User.find_by(username=addressee)
    if linkman is not None:
        m = Mail.new(form, sender_id=u.id, receiver_id=linkman.id, sender=u.username)
        m.save()
        return redirect(url_for(".index"))
    else:
        return abort(401, 'linkman error')


@main.route("/", methods=["GET"])
def index():
    u = current_user()
    if u is not None:
        send_mail = Mail.find_all(sender_id=u.id)
        markread_mail = Mail.find_all(receiver_id=u.id, read=True)
        new_mail = Mail.find_all(receiver_id=u.id, read=False)
        t = render_template(
            "mail/index.html",
            sends=send_mail,
            markread=markread_mail,
            new_mail=new_mail,
            user=u,
            )
        return t
    else:
        return abort(401, 'forbidden!')


@main.route("/view/<int:id>")
def view(id):
    mail = Mail.find(id)
    if current_user().id == mail.receiver_id:
        mail.mark_read()
        return render_template('mail/detail.html',mail=mail)
    else:
        return redirect(url_for('.index'))


