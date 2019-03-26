from objects import Object


class Tree(Object):
    """
    This typeclass describes a harvestable tree.
    """
    def at_object_creation(self):
        self.locks.add("get:false()")
        self.db.get_err_msg("You can't pick up {0}. Try chopping it with an axe instead!".format(self.name))
