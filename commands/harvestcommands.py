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

    def parse(self):
        "Simple parser to get a target."
        self.target = self.args.strip()

    def func(self):
        "This does the chopping!"

        caller = self.caller
        location = caller.location

        if not self.target:
            caller.msg("You need to specify a tree to chop!")
        else:
            target = caller.search(self.target)
            if not target:
                return
            caller.msg("You swing your axe into {0}, leaving a sizeable impression.".format(target.name))
            string = "Chips of wood fly everywhere as {0} swings their axe into {1}.".format(caller.name, target.name)
            location.msg_contents(string, exclude=[caller])
