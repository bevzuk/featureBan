import unittest

from featureBan.domain.player import Player
from featureBan.domain.card import Card


class CardTests(unittest.TestCase):
    def test_ByDefault_IsNotBlocked(self):
        c = Card()
        self.assertFalse(c.IsLocked)

    def test_CanLockCard(self):
        c = Card()
        c.lock()
        self.assertTrue(c.IsLocked)

    def test_CanUnlockCard(self):
        c = Card()
        c.lock()

        c.unlock()

        self.assertFalse(c.IsLocked)

    def test_CanAssignCard(self):
        c = Card()
        player = Player("Homer")

        c.assign_to(player)

        self.assertEqual(c.AssignedTo, "Homer")
