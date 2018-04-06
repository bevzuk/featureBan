from featureBan.domain.column import Column
from featureBan.domain.game import Game


class GameBuilder(object):
    _inbox_cards = []
    _development_cards = []
    _testing_cards = []
    _development_wip_limit = None
    _testing_wip_limit = None

    def with_inbox_column(self, cards):
        self._inbox_cards = cards
        return self

    def with_development_column(self, cards):
        self._development_cards = cards
        return self

    def with_development_column(self, cards, wip_limit=None):
        self._development_cards = cards
        self._development_wip_limit = wip_limit
        return self

    def with_testing_column(self, cards, wip_limit=None):
        self._testing_cards = cards
        self._testing_wip_limit = wip_limit
        return self

    def please(self):
        inbox_column = self._create_column(self._inbox_cards)
        development_column = self._create_column(self._development_cards, self._development_wip_limit)
        testing_column = self._create_column(self._testing_cards, self._testing_wip_limit)
        return Game([inbox_column, development_column, testing_column, Column()])

    @staticmethod
    def _create_column(cards, wip_limit=None):
        column = Column(0, wip_limit)
        for card in cards:
            column.push(card)
        return column
