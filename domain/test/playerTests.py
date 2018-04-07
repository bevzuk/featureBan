import unittest

import numpy as np

from featureBan.domain.card import Card
from featureBan.domain.coin import Coin
from featureBan.domain.player import Player
from featureBan.domain.test.coinStub import CoinStub
from featureBan.domain.test.dsl.create import Create

COIN_TAILS = CoinStub(1)
COIN_HEADS = CoinStub(0)


class PlayerTests(unittest.TestCase):
    def test_PlayerMustHaveName(self):
        homer = Player("Homer")
        self.assertEqual(homer.Name, "Homer")

    def test_Play_CoinFlipsTails_StartsNewCard(self):
        homer = Player("Homer")
        game = Create.game() \
            .with_inbox_column([Card()]) \
            .please()

        homer.play(game, COIN_TAILS)

        self.assertEqual(game.column("Development").Cards, [Card("Homer")])

    def test_Play_CoinFlipsTails_HasAssignedCardInDevelopment_MovesTheCardToTesting(self):
        homer = Player("Homer")
        game = Create.game() \
            .with_development_column([Card("Homer")]) \
            .please()

        homer.play(game, COIN_TAILS)

        self.assertEqual(game.column("Development").Cards, [])
        self.assertEqual(game.column("Testing").Cards, [Card("Homer")])

    def test_Play_CoinFlipsTails_HasAssignedCardInTesting_MovesTheCardToDone(self):
        homer = Player("Homer")
        game = Create.game() \
            .with_testing_column([Card("Homer")]) \
            .please()

        homer.play(game, COIN_TAILS)

        self.assertEqual(game.column("Testing").Cards, [])
        self.assertEqual(game.column("Done").Cards, [Card("Homer")])

    def test_Play_CoinFlipsTails_HasAssignedBlockedCardInTesting_UnblocksTheCard(self):
        homer = Player("Homer")
        game = Create \
            .game() \
            .with_testing_column([Card("Homer", True)]) \
            .please()

        homer.play(game, COIN_TAILS)

        self.assertEqual(game.column("Testing").Cards, [Card("Homer", False)])

    def test_Play_CoinFlipsHeads_HasNoCards_StartsNewCard(self):
        homer = Player("Homer")
        game = Create \
            .game() \
            .with_inbox_column([Card()]) \
            .please()

        homer.play(game, COIN_HEADS)

        self.assertEqual(game.column("Development").Cards, [Card("Homer")])

    def test_Play_CoinFlipsHeads_HasCardInDevelopment_BlocksTheCardAndStartsNewCard(self):
        homer = Player("Homer")
        game = Create \
            .game() \
            .with_inbox_column([Card()]) \
            .with_development_column([Card("Homer", False)]) \
            .please()

        homer.play(game, COIN_HEADS)

        self.assertEqual(game.column("Development").Cards, [Card("Homer", True), Card("Homer", False)])

    def test_Play_CoinFlipsTails_HasNoCards_DoNothing(self):
        homer = Player("Homer")
        game = Create \
            .game() \
            .please()

        homer.play(game, COIN_TAILS)

        self.assertEqual(game.column("Development").Cards, [])
        self.assertEqual(game.column("Testing").Cards, [])

    def test_Play_CoinFlipsHeads_HasNoCards_DoNothing(self):
        homer = Player("Homer")
        game = Create \
            .game() \
            .please()

        homer.play(game, COIN_HEADS)

        self.assertEqual(game.column("Development").Cards, [])
        self.assertEqual(game.column("Testing").Cards, [])

    def test_PlayWithWipLimits_CoinFlipsHeads_RespectWipLimit(self):
        homer = Player("Homer")
        game = Create.game() \
            .with_inbox_column([Card()]) \
            .with_development_column(cards=[Card("Homer", True)], wip_limit=1) \
            .with_testing_column(cards=[Card("Homer", True)], wip_limit=1) \
            .please()

        homer.play(game, COIN_HEADS)

        self.assertEqual(game.column("Development").Cards, [Card("Homer", True)])
        self.assertEqual(game.column("Testing").Cards, [Card("Homer", True)])

    def test_PlayWithWipLimits_CoinFlipsHeads_BlockAndRespectWipLimit(self):
        homer = Player("Homer")
        game = Create.game() \
            .with_inbox_column([Card()]) \
            .with_development_column(cards=[Card("Homer", False)], wip_limit=1) \
            .with_testing_column(cards=[Card("Homer", True)], wip_limit=1) \
            .please()

        homer.play(game, COIN_HEADS)

        self.assertEqual(game.column("Development").Cards, [Card("Homer", True)])
        self.assertEqual(game.column("Testing").Cards, [Card("Homer", True)])

    def test_PlayWithWipLimits_CoinFlipsTails_HelpOthersWithTestingIfCanNotWorkOnMyCards(self):
        homer = Player("Homer")
        game = Create.game() \
            .with_inbox_column([Card()]) \
            .with_development_column(cards=[Card("Homer")], wip_limit=1) \
            .with_testing_column(cards=[Card("Marge")], wip_limit=1) \
            .please()

        homer.play(game, COIN_TAILS)

        self.assertEqual(game.column("Development").Cards, [Card("Homer")])
        self.assertEqual(game.column("Testing").Cards, [])
        self.assertEqual(game.column("Done").Cards, [Card("Marge")])

    def test_PlayWithWipLimits_CoinFlipsTails_HelpOthersWithDevelopmentIfCanNotWorkOnMyCards(self):
        homer = Player("Homer")
        game = Create.game() \
            .with_inbox_column([Card()]) \
            .with_development_column(cards=[Card("Marge")], wip_limit=1) \
            .with_testing_column(cards=[], wip_limit=1) \
            .please()

        homer.play(game, COIN_TAILS)

        self.assertEqual(game.column("Development").Cards, [])
        self.assertEqual(game.column("Testing").Cards, [Card("Marge")])
        self.assertEqual(game.column("Done").Cards, [])

    @staticmethod
    def test_Play_WithoutLimits():
        homer = Player("Homer")
        marge = Player("Marge")
        bart = Player("Bart")
        liza = Player("Liza")
        maggie = Player("Maggie")
        coin = Coin()
        done_cards = []

        for game_count in range(1000):
            inbox = []
            for card_count in range(20):
                inbox.append(Card())
            game = Create.game() \
                .with_inbox_column(inbox) \
                .with_development_column([], 1) \
                .with_testing_column([], 1) \
                .please()

            for steps_count in range(20):
                homer.play(game, coin)
                marge.play(game, coin)
                bart.play(game, coin)
                liza.play(game, coin)
                maggie.play(game, coin)

            done_cards.append(len(game.column("Done").Cards))

        print(done_cards)
        print(np.mean(done_cards))
