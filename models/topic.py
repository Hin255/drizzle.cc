from models.mongua import Mongua
from models.user import User
from models.reply import Reply

class Topic(Mongua):
    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('views', int, 0),
            ('title', str, ''),
            ('content', str, ''),
            ('user_id', int, 0),
            ('board_id', int, 0),
        ]
        return names

    @classmethod
    def get(cls, id):
        m = cls.find_by(id=id)
        m.views += 1
        m.save()
        return m

    def replies(self):
        from .reply import Reply
        ms = Reply.find_all(topic_id=self.id)
        return ms

    def board(self):
        from .board import Board
        m = Board.find(self.board_id)
        return m

    def user(self):
        u = User.find(id=self.user_id)
        return u

    def delete_correlation_replies(self):
        replies = Reply.find_all(topic_id=self.id)
        for r in replies:
            r.delete()


    # @classmethod
    # def topic_sum(cls, id):
    #     u = User.find_by(id=id)
    #     ms = cls.find_all(user_id=u.id)
    #     u.topic_amount = 0
    #     for m in ms:
    #         u.topic_amount += 1
    #     u.save()
    #     return u
