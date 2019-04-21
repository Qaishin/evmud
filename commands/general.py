"""
Item related commands module.

"""
from evennia import CmdSet
from evennia.commands.default.muxcommand import MuxCommand


class GeneralCmdSet(CmdSet):
    """ Command set for general related commands. """
    key = 'general_cmdset'
    priority = 1

    def at_cmdset_creation(self):
        pass
