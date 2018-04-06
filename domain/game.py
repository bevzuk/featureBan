from functools import reduce

from featureBan.domain.column import Column


class Game(object):
    _columns = {}

    def __init__(self, columns=None):
        if columns is None or not columns:
            columns = [Column(10), Column(), Column(), Column()]

        self._columns = {
            "Inbox": columns[0],
            "Development": columns[1],
            "Testing": columns[2],
            "Done": columns[3]
        }

    def column(self, name):
        return self._columns[name]

    def get_new_card(self, player):
        if self.column("Development").is_wip_limit_reached():
            return

        card = self.column("Inbox").pull()
        if card is not None:
            card.assign_to(player)
            self.column("Development").push(card)

    def get_card_assigned_to(self, player):
        for card in self.column("Testing").Cards:
            if card.AssignedTo == player.Name:
                return card

        for card in self.column("Development").Cards:
            if card.AssignedTo == player.Name:
                return card

        return None

    def get_card_not_assigned_to(self, player):
        for card in self.column("Testing").Cards:
            if card.AssignedTo != player.Name:
                return card

        for card in self.column("Development").Cards:
            if card.AssignedTo != player.Name:
                return card

        return None

    def get_unlocked_card_assigned_to(self, player):
        for card in self.column("Testing").Cards:
            if card.AssignedTo == player.Name and not card.IsLocked:
                return card

        for card in self.column("Development").Cards:
            if card.AssignedTo == player.Name and not card.IsLocked:
                return card

        return None

    def move_right(self, card):
        right_to_left_wip_columns = reversed(list(enumerate(self._columns.items()))[1:-1])
        for i, column in right_to_left_wip_columns:
            if card in column[1].Cards:
                self._pull(card, i + 1)
                return

    def _pull(self, card, column_index):
        self._get_column_by_index(column_index - 1).Cards.remove(card)
        self._get_column_by_index(column_index).Cards.append(card)

    def _get_column_by_index(self, column_index):
        return list(self._columns.items())[column_index][1]

    def __str__(self):
        max_cards_count = max(map(lambda x: len(x[1].Cards), list(self._columns.items())))
        str = "".join("{:20}".format(k) for k in self._columns.keys()) + "\n"
        for row in range(max_cards_count):
            line = ""
            for column in self._columns.items():
                if row < len(column[1].Cards):
                    card = column[1].Cards[row]
                    card_str = "[" + card.AssignedTo + " " + ("B" if card.IsLocked else " ") + "]"
                    line += "{0:20}".format(card_str)
                else:
                    line += "{:20}".format("")
            line += "\n"
            str += line
        return str
        # return max(map(lambda x: len(x[1]), self._columns))
