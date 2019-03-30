"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia import DefaultCharacter


class Character(DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.

    """
    def at_init(self):
        # Is the player currently harvesting a resource?
        self.ndb.harvesting = False
        # If harvesting is interrupted, such as by moving to a different room,
        # a callback may be supplied that can be called upon interruption.
        self.ndb.harvesting_interrupt = None

    def at_before_move(self, destination, **kwargs):
        # If we were in the middle of harvesting, it needs to be cancelled.
        if self.ndb.harvesting:
            self.ndb.harvesting = False
            # If we set an interrupting callback, call it now.
            if self.ndb.harvesting_interrupt:
                self.ndb.harvesting_interrupt()
                self.ndb.harvesting_interrupt = None
        return True
