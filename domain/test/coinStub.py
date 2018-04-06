class CoinStub(object):
    def __init__(self, flip_value):
        self._flipValue = flip_value

    def flip(self):
        return self._flipValue
