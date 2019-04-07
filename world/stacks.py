"""
Item Stacking Handler

This implements item stacking functionality for objects. The stack is
instantiated by a `StackHandler` object, which is set up as a property
on the object typeclass.

**Setup**
    To use item stacks on an object, add a function that passes the object
    itself into the constructor and returns a `StackHandler`. This function
    should be decorated with the `lazy_property` decorator.
"""


class StackHandler:
    """
    Factory class that instantiates stacks on objects.

    Args:
        obj (Object): parent Object typeclass for this StackHandler
    """
    def __init__(self, obj):
        if not obj.attributes.has('stack'):
            obj.attributes.add('stack',
                               {
                                'stackable': False,
                                'count': 1
                               })
        self.attr_dict = obj.attributes.get('stack')
        self.obj = obj

    def get_stackable(self):
        "Is the object this handler is attached to stackable?"
        return self.attr_dict['stackable']

    def set_stackable(self, value):
        if type(value) != bool:
            raise AttributeError("Value set for stackable must be True or False.")
        self.attr_dict['stackable'] = value
        self.attr_dict['count'] = 1

    stackable = property(get_stackable, set_stackable)

    def get_count(self):
        return self.attr_dict['count']

    def set_count(self, amount):
        self.attr_dict['count'] = amount

    count = property(get_count, set_count)

    def split(self, amount):
        """
        Splits this stack into another stack. If the split amount is greater than
        or equal to the total stack count, then return the same object. Otherwise,
        return a newly created stack.

        Args:
            amount: Amount to split this stack by.

        Returns:
            copy (Object): New object stack with appropriate amount if split amount is less than
                current stack count, otherwise returns same object.
        """
        if amount >= self.count:
            return self.obj
        else:
            return self.obj.copy(new_key=self.obj.key)
            self.attr_dict['count'] -= amount

    def merge(self, obj):
        "Merge given object stack into this one."
        self.attr_dict['count'] += obj.stack.count
        del obj

    def consume(self, amount):
        """
        Consume a given amount of items from the stack. If the stack count
        reaches 0 or less, then the parent object should be destroyed.

        Args:
            amount: Amount to consume from this stack.
        """
        self.attr_dict['count'] -= amount
        if self.count <= 0:
            del self.obj
