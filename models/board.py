import time
from models.mongua import Mongua

class Board(Mongua):

    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('title', str, ''),
        ]
        return names