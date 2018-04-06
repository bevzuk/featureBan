from featureBan.domain.test.dsl.gameBuilder import GameBuilder


class Create(object):
    @staticmethod
    def game():
        return GameBuilder()