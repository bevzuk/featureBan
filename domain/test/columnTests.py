import unittest

from featureBan.domain.card import Card
from featureBan.domain.column import Column


class ColumnTests(unittest.TestCase):
    def test_ByDefault_ColumnHasNoCards(self):
        column = Column()
        self.assertEqual(len(column.Cards), 0)

    def test_CanHaveCards(self):
        column = Column(10)
        self.assertEqual(len(column.Cards), 10)

    def test_CanPushCardsIndependently(self):
        column1 = Column()
        column2 = Column()

        column1.push(Card())

        self.assertEqual(len(column1.Cards), 1)
        self.assertEqual(len(column2.Cards), 0)

    def test_CanPullCard(self):
        column1 = Column(1)
        column2 = Column()

        column2.pull_from(column1)

        self.assertEqual(len(column1.Cards), 0)
        self.assertEqual(len(column2.Cards), 1)

    def test_CanNotPullBlockedCard(self):
        column1 = Column()
        card = Card()
        card.lock()
        column1.push(card)
        column2 = Column()

        column2.pull_from(column1)

        self.assertEqual(len(column1.Cards), 1)
        self.assertEqual(len(column2.Cards), 0)

    def test_CanNotPullCard_BreakingWipLimit(self):
        column1 = Column(number_of_cards=1)
        column2 = Column(number_of_cards=1, wip_limit=1)

        column2.pull_from(column1)

        self.assertEqual(len(column1.Cards), 1)
        self.assertEqual(len(column2.Cards), 1)


