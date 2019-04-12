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
        self.add(CmdSay())


class CmdSay(MuxCommand):
    """
    speak as your character

    Usage:
      say <message>

    Talk to those in your current location.
    """

    key = "say"
    aliases = ['"', "'"]
    locks = "cmd:all()"

    def func(self):
        """Run the say command"""

        caller = self.caller

        if not self.args:
            caller.msg("Say what?")
            return

        speech = self.args

        # Calling the at_before_say hook on the character
        speech = caller.at_before_say(speech)

        # If speech is empty, stop here
        if not speech:
            return

        # Call the at_after_say hook on the character
        caller.at_say(speech, msg_self=True, mapping={"object": caller.db.sdesc})
