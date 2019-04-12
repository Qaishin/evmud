"""
Item

The Object is the base typeclass for implementing in-game items.

"""
from evennia.utils import lazy_property
from world.stacks import StackHandler
from typeclasses.objects import Object


class Item(Object):
    """
    This is the root typeclass object for implmenting in-game items.
    """

    def at_object_creation(self):
        super().at_object_creation()
        self.db.ldesc = f"{self.get_numbered_name(1, None, key=self.db.sdesc)[0]} is here".capitalize()

    @lazy_property
    def stack(self):
        """ StackHandler that manages stacks. """
        return StackHandler(self)
