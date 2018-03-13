# from models import Model
from models.mongua import Mongua
from utils import log
import re
Model = Mongua


class User(Model):

    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('username', str, ''),
            ('password', str, ''),
            ('nickname', str, ''),
            ('user_image', str, '/uploads/default.png'),
            ('topic_amount', int, 0),
            ('signature', str, '无签名'),
            ('email', str, ''),
        ]
        return names

    def salted_password(self, password, salt='$!@><?>HUI&DWQa`'):
        import hashlib
        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()

        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    def hashed_password(self, pwd):
        import hashlib
        p = pwd.encode('ascii')
        s = hashlib.sha256(p)
        return s.hexdigest()

    @classmethod
    def validate_string(cls, string):
        x = True
        while x:
            if (len(string) < 6 or len(string) > 20):
                break
            elif not re.search("[a-z]", string):
                break
            elif not re.search("[0-9]", string):
                break
            # elif not re.search("[A-Z]", string):
            #     break
            # elif not re.search("[$#@]", string):
            #     break
            # elif re.search("\s", string):
            #     break
            else:
                x = False
                break

        if x:
            return False
        else:
            return True

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        pwd = form.get('password', '')

        if cls.validate_string(pwd) and User.find_by(username=name) is None:
            u = User.new(form)
            u.password = u.salted_password(pwd)
            u.save()
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        username = form.get('username')
        password = form.get('password')
        user = User.find_by(username=username)
        if user is not None and user.password == user.salted_password(password):
            return user
        else:
            return None
