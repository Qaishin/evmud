"""
Room

Rooms are simple containers that has no location of their own.

"""
from collections import defaultdict
from evennia import DefaultRoom
from evennia.utils import list_to_string, justify
from typeclasses.objects import Object

CARDINAL_SORT = {'north': 0,
                 'northeast': 1,
                 'east': 2,
                 'southeast': 3,
                 'south': 4,
                 'southwest': 5,
                 'west': 6,
                 'northwest': 7,
                 'up': 8,
                 'down': 9,
                 'in': 10,
                 'out': 11}


class Room(Object, DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """

    def return_appearance(self, looker, **kwargs):
        """
        This formats a description. It is the hook a 'look' command
        should call.

        Args:
            looker (Object): Object doing the looking.
            **kwargs (dict): Arbitrary, optional arguments for users
                overriding the call (unused by default).
        """
        if not looker:
            return ""
        # get and identify all objects
        visible = (con for con in self.contents if con != looker and
                   con.access(looker, "view"))
        exits, users, things = [], [], defaultdict(list)
        for con in visible:
            key = con.get_display_name(looker)
            if con.destination:
                exits.append(con.name)
            elif con.has_account:
                users.append("%s" % key)
            else:
                # things can be pluralized
                things[key].append(con)
        # get description, build string
        # string = "|Y%s|n\n" % self.get_display_name(looker)
        string = ""
        desc = self.db.desc
        if desc:
            string += "%s |C" % desc
        if users or things:
            # handle pluralization of things (never pluralize users)
            thing_strings = []
            for key, itemlist in sorted(things.items()):
                nitem = len(itemlist)
                if nitem == 1:
                    try:
                        if itemlist[0].stack.stackable and itemlist[0].stack.count > 1:
                            # key = itemlist[0].get_numbered_name(itemlist[0].stack.count, looker, key=key)[1]
                            sdesc = itemlist[0].get_numbered_name(itemlist[0].stack.count, looker,
                                                                  key=itemlist[0].db.sdesc)[1]
                            key = f"There are {sdesc} here. "
                        else:
                            # key, _ = itemlist[0].get_numbered_name(nitem, looker, key=key)
                            key = itemlist[0].db.ldesc + ". "
                    except AttributeError:
                        # key, _ = itemlist[0].get_numbered_name(nitem, looker, key=key)
                        key = itemlist[0].db.ldesc + ". "

                else:
                    # key = [item.get_numbered_name(nitem, looker, key=key)[1] for item in itemlist][0]
                    sdesc = [item.get_numbered_name(nitem, looker, key=item.db.sdesc)[1] for item in itemlist][0]
                    key = f"There are {sdesc} here. "
                thing_strings.append(key)

            if thing_strings:
                # string += "|CYou see " + list_to_string(thing_strings) + ". "
                for s in thing_strings:
                    string += s

            for user in users:
                string += f"|c{user} is here. |n"

        #  Do some pretty formatting here for the room description, objects, and players.
        string = justify(string, align="l", width=120)
        splitstring = string.split('\n', 1)
        if (len(splitstring) == 2):
            string = splitstring[0] + '\n' + justify(splitstring[1], align="l", width=119, indent=1)
        #for i, s in enumerate(splitstring):
        #    if i < 1:
        #        string += s
        #        if i < len(splitstring) - 1:
        #            string += "\n"
        #    else:
        #        string += " " + s
        #        if i < len(splitstring) - 1:
        #            string += "\n"

        if exits:
            if len(exits) > 1:
                sort_list = [CARDINAL_SORT[ex] if ex in CARDINAL_SORT else 13 for ex in exits]
                sorted_exits = [x for _, x in sorted(zip(sort_list, exits))]
                string += "\n|YYou see exits leading " + list_to_string(sorted_exits) + ".|n"
            else:
                string += "\n|YYou see a single exit leading " + exits[0] + ".|n"

        # return "|Y%s.|n\n" % self.get_display_name(looker) + string
        return f"|Y{self.get_display_name(looker)}.|n\n{string}"
