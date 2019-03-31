"""
Commands

Commands describe the input the account can do to the game.

"""

from evennia import Command
from typeclasses.harvestables import Tree


def stop_harvesting(character):
    character.ndb.harvesting = False
    character.ndb.harvesting_interrupt = None


class CmdStop(Command):
    """
    Stops current timed harvest command.

    Usage:
        stop

    This will stop any harvesting command currently being used,
    such as chopping trees or digging.
    """
    key = "stop"
    help_category = "harvesting"

    def func(self):
        if not self.caller.ndb.harvesting:
            self.caller.msg("You are not currently harvesting anything...")
        else:
            self.caller.msg("You cease harvesting activities.")
            stop_harvesting(self.caller)


class CmdChop(Command):
    """
    Chop trees.

    Usage:
        chop [target]

    This will use an axe in your inventory to chop a tree.
    """
    key = "chop"
    aliases = ["chop down"]
    help_category = "harvesting"

    def parse(self):
        "Simple parser to get a target."
        self.target = self.args.strip()

    def func(self):
        "This does the chopping!"

        caller = self.caller

        if caller.ndb.harvesting:
            caller.msg("You are already in the middle of harvesting!")
            return

        if not self.target:
            caller.msg("You need to specify a tree to chop!")
            return

        target = caller.search(self.target)
        if not target:
            return

        if not (isinstance(target, Tree) and target.access(caller, "chop")):
            caller.msg("You are unable to chop down {0}!".format(target.name))
            return

        # Code elsewhere may need to interrupt our tree chopping madness, such as
        # moving to another room. This provides a callback that gives a sensible message
        # indicating that we were interrupted unexpectedly.
        def interrupt_callback():
            caller.msg("You are interrupted and fail to finish chopping down {0}".format(target.name))
        caller.ndb.harvesting_interrupt = interrupt_callback

        caller.ndb.harvesting = True

        while caller.ndb.harvesting:
            # The tree was destroyed already, exit gracefully.
            if not target.pk:
                stop_harvesting(caller)
                return

            caller.msg("Chips of wood fly everywhere as you swing your axe into {0}.".format(target.name))
            string = "Chips of wood fly everywhere as {0} swings their axe into {1}.".format(caller.name,
                                                                                             target.name)
            caller.location.msg_contents(string, exclude=[caller])
            if target.chop(5):
                stop_harvesting(caller)
                return
            elif target.hp <= target.max_hp / 4:
                caller.msg("{0} is beginning to lean heavily.".format(target.name))
            elif target.hp <= target.max_hp / 2:
                caller.msg("There is a sizeable wedge in {0}".format(target.name))

            yield 2

        stop_harvesting(caller)
