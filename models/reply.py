from models.mongua import Mongua

Model = Mongua


class Reply(Model):
    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('content', str, ''),
            ('topic_id', int, 0),
            ('user_id', int, 0),
        ]
        return names

    def user(self):
        from .user import User
        u = User.find(self.user_id)
        return u
