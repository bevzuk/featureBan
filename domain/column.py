from featureBan.domain.card import Card


class Column(object):
    _wip_limit = 0
    Cards = []

    def __init__(self, number_of_cards=0, wip_limit=0):
        self._wip_limit = wip_limit
        self.Cards = []
        for i in range(number_of_cards):
            self.Cards.append(Card())

    def pull(self):
        for card in self.Cards:
            if not card.IsLocked:
                self.Cards.remove(card)
                return card
        return None

    def pull_from(self, previous_column):
        if 0 < self._wip_limit <= len(self.Cards):
            return

        card = previous_column.pull()
        if card is not None:
            self.push(card)

    def push(self, card):
        self.Cards.append(card)

    def is_wip_limit_reached(self):
        return self._wip_limit is not None and self._wip_limit <= len(self.Cards)

    def __str__(self):
        s = ""
        for card in self.Cards:
            s += "[" + card.AssignedTo + " " + ("B" if card.IsLocked else " ") + "]\n"
        return s
