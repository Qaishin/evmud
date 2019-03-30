"""
Crafting Components

Crafting Components are Objects which are obtained through harvesting
or other means by the Player, and may be crafted into other items or
used in building.

"""
from typeclasses.objects import Object


class CraftingComponent(Object):
    pass


COMPONENT_PROTOTYPES = {
    "log": {
        "typeclass": "typeclasses.craftingcomponents.CraftingComponent",
        "key": "Log",
        "desc": "A generic log."
    }
}
