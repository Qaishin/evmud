"""
Commands

Commands describe the input the account can do to the game.

"""

from evennia import Command


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
        location = caller.location

        if not self.target:
            caller.msg("You need to specify a tree to chop!")
            return

        target = caller.search(self.target)
        if not target:
            return

        if not target.access(caller, "chop"):
            caller.msg("You are unable to chop {0}!".format(target.name))
            return

        caller.msg("You swing your axe into {0}, leaving a sizeable impression.".format(target.name))
        string = "Chips of wood fly everywhere as {0} swings their axe into {1}.".format(caller.name, target.name)
        location.msg_contents(string, exclude=[caller])
