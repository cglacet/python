from textwrap import indent


class Zipper:
    def __init__(self, focus=None, context=None):
        self.focus = focus
        self.context = context or []

    @property
    def value(self):
        try:
            return self.focus.value
        except AttributeError as attribute:
            raise ValueError("There is no value here, but you can insert a node here.") from attribute

    def set_value(self, value):
        new_left = self.focus.left or None
        new_right = self.focus.right or None
        new_location = Zipper(Focus(value, new_left, new_right), self.context)
        new_location.focus.value = value
        return new_location

    @property
    def left(self):
        new_focus, new_context = self.focus.focus_left()
        return Zipper(new_focus, self.context+[new_context])

    @property
    def right(self):
        new_focus, new_context = self.focus.focus_right()
        return Zipper(new_focus, self.context+[new_context])

    @property
    def up(self):
        last_context = self.context[-1]
        previous_focus = last_context.reattach(self.focus)
        return Zipper(previous_focus, self.context[:-1])

    @property
    def tree(self):
        return self.root.focus

    @property
    def root(self):
        zipper = Zipper(self.focus, self.context)
        while zipper.context:
            zipper = zipper.up
        return zipper

    def insert(self, obj):
        focus = None
        # Both `Zipper` and `Focus` obj instances are not tested in zipper_test.py
        # We could suggest this as optional things to do:
        if isinstance(obj, Zipper):
            focus = obj.tree
        elif isinstance(obj, Focus):
            focus = obj
        else:
            # This is the tested behavior:
            focus = Focus(obj, None, None)
        return Zipper(focus, self.context)

    # These two are not tested either, they could also be suggested as optional
    # things to do
    def insert_left(self, obj):
        return self.left.insert(obj).up

    def insert_right(self, obj):
        return self.right.insert(obj).up

    def __repr__(self):
        context_str = '('+'), ('.join(map(str, self.context))+')'
        return f"focus:\n{self.focus}\ncontext:[\n{context_str}\n]"


class BinaryTree:
    def __init__(self, value, left, right):
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        text = str(self.value)
        if self.left:
            text += '\n L:' + indent(str(self.left), '  ')
        if self.right:
            text += '\n R:' + indent(str(self.right), '  ')
        return text


class Context(BinaryTree):
    def __init__(self, value, left, right, is_left=False):
        self.is_left = is_left
        super().__init__(value, left, right)

    def reattach(self, tree):
        if self.is_left:
            return Focus(self.value, tree, self.right)
        return Focus(self.value, self.left, tree)


class Focus(BinaryTree):
    def focus_left(self):
        return self.left, Context(self.value, None, self.right, is_left=True)

    def focus_right(self):
        return self.right, Context(self.value, self.left, None)
