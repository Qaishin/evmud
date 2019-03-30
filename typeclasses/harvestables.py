from typeclasses.objects import Object


class Tree(Object):
    """
    This typeclass describes a harvestable tree.
    """
    def at_object_creation(self):
        self.locks.add("get:false();chop:all()")
        self.db.get_err_msg = "You can't pick {0} up. Try chopping it with an axe instead!".format(self.name)
        self.db.max_hp = 20
        self.db.hp = 20

    @property
    def hp(self):
        return self.db.hp

    @property
    def max_hp(self):
        return self.db.max_hp

    def chop(self, amount):
        """
        Chop a tree by a specified amount of 'hp'. If hp drops at
        or below 0, spawn appropriate stack of logs and delete the tree.

        Return True if tree is completed destroyed, False if otherwise.
        """
        self.db.hp -= amount

        if self.db.hp <= 0:
            # spawn logs
            self.location.msg_contents("{0} makes a loud cracking sound and falls to the ground.".format(self.name))
            self.delete()
            return True
        else:
            return False
