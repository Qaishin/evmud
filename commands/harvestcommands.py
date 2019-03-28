"""
Commands

Commands describe the input the account can do to the game.

"""

from evennia import Command, create_script
from typeclasses.harvestables import Tree, stop_harvests


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
        stop_harvests(self.caller)


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

        if not self.target:
            caller.msg("You need to specify a tree to chop!")
            return

        target = caller.search(self.target)
        if not target:
            return

        if not (isinstance(target, Tree) and target.access(caller, "chop")):
            caller.msg("You are unable to chop down {0}!".format(target.name))
            return

        create_script('harvestables.TreeChopScript', obj=caller, attributes=[('target', target)])
