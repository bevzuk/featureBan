import random


class Coin(object):
    def __init__(self):
        random.seed()

    @staticmethod
    def flip():
        return random.randint(0, 1)
