"""
Item related commands module.

"""
from evennia import CmdSet
from evennia.commands.default.muxcommand import MuxCommand
from evennia.utils import evtable


class ItemCmdSet(CmdSet):
    """ Command set for item related commands. """
    key = 'harvest_cmdset'
    priority = 1

    def at_cmdset_creation(self):
        self.add(CmdInventory())
        self.add(CmdGet())
        self.add(CmdDrop())
        self.add(CmdGive())


class CmdInventory(MuxCommand):
    """
    view inventory

    Usage:
      inventory
      inv

    Shows your inventory.
    """
    key = "inventory"
    aliases = ["inv", "i"]
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        """check inventory"""
        items = self.caller.contents
        if not items:
            string = "You are not carrying anything."
        else:
            table = evtable.EvTable(border="header")
            for item in items:
                if item.stack.stackable:
                    table.add_row(f"|C{item.name}|n|w(|g{item.stack.count}|w)|n", item.db.desc or "")
                else:
                    table.add_row(f"|C{item.name}|n", item.db.desc or "")
            string = "|wYou are carrying:\n%s" % table
        self.caller.msg(string)


class CmdGet(MuxCommand):
    """
    pick up something

    Usage:
      get [amount] <obj>

    Picks up an object from your location and puts it in
    your inventory.
    """
    key = "get"
    aliases = "grab"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def parse(self):
        super().parse()

        self.target = self.args
        self.amount = 1

        if len(self.arglist) > 1:
            try:
                self.amount = int(self.arglist[0])
                if self.amount <= 0:
                    self.amount = 1
                self.target = " ".join(self.arglist[1:])
            except ValueError:
                pass

    def func(self):
        """implements the command."""

        caller = self.caller
        if not self.args:
            caller.msg("Get what?")
            return

        obj = caller.search(self.target, location=caller.location)

        if not obj:
            return

        if caller == obj:
            caller.msg("You can't get yourself.")
            return

        if not obj.access(caller, 'get'):
            if obj.db.get_err_msg:
                caller.msg(obj.db.get_err_msg)
            else:
                caller.msg("You can't get that.")
            return

        # calling at_before_get hook method
        if not obj.at_before_get(caller):
            return

        if obj.stack.stackable:
            obj = obj.stack.split(self.amount)

            caller.msg(f"You pick up {obj.stack.count} {obj.name}{'s' if self.amount > 1 else ''}.")
            caller.location.msg_contents(f"{caller.name} picks up {obj.stack.count} {obj.name}"
                                         f"{'s' if self.amount > 1 else ''}.", exclude=caller)
        else:
            caller.msg(f"You pick up {obj.name}.")
            caller.location.msg_contents(f"{caller.name} picks up {obj.name}.", exclude=caller)

        obj.move_to(caller, quiet=True)

        # calling at_get hook method
        obj.at_get(caller)


class CmdDrop(MuxCommand):
    """
    drop something

    Usage:
      drop [amount] <obj>

    Lets you drop an object from your inventory into the
    location you are currently in.
    """

    key = "drop"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def parse(self):
        super().parse()

        self.target = self.args
        self.amount = 1

        if len(self.arglist) > 1:
            try:
                self.amount = int(self.arglist[0])
                if self.amount <= 0:
                    self.amount = 1
                self.target = " ".join(self.arglist[1:])
            except ValueError:
                pass

    def func(self):
        """Implement command"""

        caller = self.caller
        if not self.args:
            caller.msg("Drop what?")
            return

        # Because the DROP command by definition looks for items
        # in inventory, call the search function using location = caller
        obj = caller.search(self.target, location=caller,
                            nofound_string="You aren't carrying %s." % self.args,
                            multimatch_string="You carry more than one %s:" % self.args)
        if not obj:
            return

        # Call the object script's at_before_drop() method.
        if not obj.at_before_drop(caller):
            return

        if obj.stack.stackable:
            obj = obj.stack.split(self.amount)
            caller.msg(f"You drop {obj.stack.count} {obj.name}"
                       f"{'s' if self.amount > 1 else ''}.")
            caller.location.msg_contents(f"{caller.name} drops {obj.stack.count} {obj.name}"
                                         f"{'s' if self.amount > 1 else ''}.", exclude=caller)
        else:
            caller.msg(f"You drop {obj.name}.")
            caller.location.msg_contents(f"{caller.name} drops {obj.name}.", exclude=caller)

        obj.move_to(caller.location, quiet=True)

        # Call the object script's at_drop() method.
        obj.at_drop(caller)


class CmdGive(MuxCommand):
    """
    give away something to someone

    Usage:
      give [amount] <inventory obj> <to||=> <target>

    Gives an items from your inventory to another character,
    placing it in their inventory.
    """
    key = "give"
    rhs_split = ("=", " to ")  # Prefer = delimiter, but allow " to " usage.
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def parse(self):
        super().parse()

        self.target = self.lhs
        self.amount = 1

        arglist = [args.strip() for args in self.lhslist[0].split()]

        if len(arglist) > 1:
            try:
                self.amount = int(arglist[0])
                if self.amount <= 0:
                    self.amount = 1
                self.target = " ".join(arglist[1:])
            except ValueError:
                pass

    def func(self):
        """Implement give"""

        caller = self.caller
        if not self.args or not self.rhs:
            caller.msg("Usage: give [amount] <inventory object> to <target>")
            return

        to_give = caller.search(self.target, location=caller,
                                nofound_string="You aren't carrying %s." % self.lhs,
                                multimatch_string="You carry more than one %s:" % self.lhs)
        target = caller.search(self.rhs)
        if not (to_give and target):
            return
        if target == caller:
            caller.msg("You keep %s to yourself." % to_give.key)
            return
        if not to_give.location == caller:
            caller.msg("You are not holding %s." % to_give.key)
            return

        # calling at_before_give hook method
        if not to_give.at_before_give(caller, target):
            return

        if to_give.stack.stackable:
            to_give = to_give.stack.split(self.amount)
            caller.msg(f"You give {to_give.stack.count} {to_give.key}{'s' if self.amount > 1 else ''}"
                       f" to {target.key}.")
            target.msg(f"{caller.key} gives you {to_give.stack.count} {to_give.name}"
                       f"{'s' if self.amount > 1 else ''}.", exclude=caller)
        else:
            caller.msg(f"You give {to_give.key} to {target.key}.")
            target.msg(f"{caller.key} gives you {to_give.name}.", exclude=caller)

        # give object
        to_give.move_to(target, quiet=True)

        # Call the object script's at_give() method.
        to_give.at_give(caller, target)
