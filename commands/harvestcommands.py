"""
Commands

Commands describe the input the account can do to the game.

"""

from evennia import Command
from typeclasses.harvestables import Tree


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
        self.caller.msg("You cease harvesting activities.")
        self.caller.ndb.harvesting = False


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

        def interrupt_callback():
            caller.msg("You are interrupted and fail to finish chopping down {0}".format(target.name))
            caller.ndb.harvesting_interrupted = False
        caller.ndb.harvesting_interrupt = interrupt_callback

        caller.ndb.harvesting = True
        first_msg = False
        second_msg = False

        while caller.ndb.harvesting:
            # The tree was destroyed already, exit gracefully.
            if not target.pk:
                caller.ndb.harvesting = False
                caller.ndb.harvesting_interrupt = None
                return

            caller.msg("Chips of wood fly everywhere as you swing your axe into {0}.".format(target.name))
            string = "Chips of wood fly everywhere as {0} swings their axe into {1}.".format(caller.name,
                                                                                             target.name)
            caller.location.msg_contents(string, exclude=[caller])
            if target.chop(5):
                caller.ndb.harvesting = False
                return
            elif target.hp <= target.max_hp / 4 and not first_msg:
                caller.msg("{0} is beginning to lean heavily.".format(target.name))
                first_msg = True
            elif target.hp <= target.max_hp / 2 and not second_msg:
                caller.msg("There is now a sizeable wedge in {0}".format(target.name))
                second_msg = True

            yield 2

        caller.ndb.harvesting_interrupt = None
