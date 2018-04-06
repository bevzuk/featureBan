class Player(object):
    def __init__(self, name):
        self.Name = name

    def play(self, game, coin):
        if game.get_card_assigned_to(self) is None:
            game.get_new_card(self)
            return

        if coin.flip() == 1:
            self._play_tails(game)
        else:
            self._play_heads(game)

    def _play_tails(self, game):
        if not self._can_do_something_with_my_cards(game):
            self._help_others(game)
            return

        card = game.get_card_assigned_to(self)
        if card.IsLocked:
            card.unlock()
        else:
            game.move_right(card)

    def _can_do_something_with_my_cards(self, game):
        card = game.get_card_assigned_to(self)
        if card is None and len(game.column("Inbox").Cards) == 0:
            return False

        if card is not None and card.IsLocked:
            return True

        if card is not None and card in game.column("Development").Cards and not game.column("Testing").is_wip_limit_reached():
            return True

        if card is not None and card in game.column("Testing").Cards:
            return True

        return False

    def _help_others(self, game):
        card = game.get_card_not_assigned_to(self)
        if card.IsLocked:
            card.unlock()
        else:
            game.move_right(card)

    def _play_heads(self, game):
        card = game.get_unlocked_card_assigned_to(self)
        if card is not None:
            card.lock()
        game.get_new_card(self)

