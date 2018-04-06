class Card(object):
    IsLocked = False
    AssignedTo = ""

    def __init__(self, name="", is_locked=False):
        self.AssignedTo = name
        self.IsLocked = is_locked

    def lock(self):
        self.IsLocked = True

    def unlock(self):
        self.IsLocked = False

    def assign_to(self, player):
        self.AssignedTo = player.Name

    def __eq__(self, other):
        return self.AssignedTo == other.AssignedTo and \
               self.IsLocked == other.IsLocked

    def __str__(self):
        return "{AssignedTo: \"" + self.AssignedTo + "\", IsLocked: " + str(self.IsLocked) + "}"
