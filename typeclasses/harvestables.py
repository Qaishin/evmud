from evennia import DefaultScript
from evennia.utils.logger import log_err
from typeclasses.objects import Object


def stop_harvests(character):
    "Stops any harvesting activity on the passed character."
    for t in character.scripts.get('treechop_script'):
        t.stop_chopping()


class TreeChopScript(DefaultScript):
    """
    Automatic tree chopping script, initiated with the chop command.
    Attached to character object.
    """
    def at_script_creation(self):
        self.key = "treechop_script"
        self.desc = "Chops down a tree"
        self.interval = 2  # 2 second intervals for harvest command
        self.persistent = False

    def at_repeat(self):
        target = self.attributes.get('target')
        if not target:
            log_err("TreeChopScript: Lost target. Character {0}".format(self.obj.name))
            self.stop()
            return

        self.obj.msg("Chips of wood fly everywhere as you swing your axe into {0}.".format(target.name))
        string = "Chips of wood fly everywhere as {0} swings their axe into {1}.".format(self.obj.name,
                                                                                         target.name)
        self.obj.location.msg_contents(string, exclude=[self.obj])
        tree_destroyed = target.chop(5)
        if tree_destroyed:
            self.stop()

    def stop_chopping(self):
        self.obj.msg("You stop chopping {0}".format(self.attributes.get('target').name))
        self.stop()


class Tree(Object):
    """
    This typeclass describes a harvestable tree.
    """
    def at_object_creation(self):
        self.locks.add("get:false();chop:all()")
        self.db.get_err_msg = "You can't pick {0} up. Try chopping it with an axe instead!".format(self.name)
        self.db.hp = 20

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
