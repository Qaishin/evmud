"""
Harvestables

Harvestables are Objects that may be harvested by players utilizing
various commands, such as chop, gather, and mine. These objects then
provide various crafting components, which are implemented through
Evennia's prototype spawning system.

"""
from evennia.prototypes.spawner import spawn
from typeclasses.objects import Object


COMPONENT_PROTOTYPES = {
    "log": {
        "typeclass": "typeclasses.harvestables.CraftingComponent",
        "key": "Log",
        "desc": "A generic log."
    }
}


class CraftingComponent(Object):
    """
    This typeclass describes a crafting component.
    """
    def at_object_creation(self):
        self.stack.stackable = True


class Tree(Object):
    """
    This typeclass describes a harvestable tree.
    """
    def at_object_creation(self):
        self.locks.add("get:false();chop:all()")
        self.db.get_err_msg = "You can't pick {0} up. Try chopping it with an axe instead!".format(self.name)
        self.db.max_hp = 20
        self.db.hp = 20
        # The crafting component prototype that should be spawned on a successful harvest.
        self.db.component_drop = "log"
        # How many components should be dropped on a successful harvest.
        self.db.component_dropamt = 3

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

            for i in range(self.db.component_dropamt):
                drop = spawn(COMPONENT_PROTOTYPES[self.db.component_drop], prototype_parents=COMPONENT_PROTOTYPES)[0]
                drop.location = self.location

            self.delete()
            return True
        else:
            return False
