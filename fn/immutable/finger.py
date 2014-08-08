"""Finger tree implementation and application examples.

A finger tree is a purely functional data structure used in
efficiently implementing other functional data structures. A
finger tree gives amortized constant time access to the "fingers"
(leaves) of the tree, where data is stored, and the internal
nodes are labeled in some way as to provide the functionality of
the particular data structure being implemented.

More information on Wikipedia: http://goo.gl/ppH2nE

"Finger trees: a simple general-purpose data structure": http://goo.gl/jX4DeL
"""

from collections import namedtuple

from fn.uniform import reduce

# data Node a = Node2 a a | Node3 a a a
# data Digit a = One a | Two a a | Three a a a | Four a a a a 
# data FingerTree a = Empty
#                   | Single a
#                   | Deep (Digit a) (FingerTree (Node a)) (Digit a)

One = namedtuple("One", "a")
Two = namedtuple("Two", "a,b")
Three = namedtuple("Three", "a,b,c")
Four = namedtuple("Four", "a,b,c,d")

class Node2(namedtuple("Node2", "a,b")):
    def __iter__(self):
        yield self.a
        yield self.b

class Node3(namedtuple("Node3", "a,b,c")):
    def __iter__(self):
        yield self.a
        yield self.b
        yield self.c

class FingerTree(object):

    class Empty(object):
        __slots__ = ("measure",)

        def __init__(self, measure):
            object.__setattr__(self, "measure", measure)

        def __setattr__(self, *args):
            raise AttributeError("Attributes of {0} object "
                                 "cannot be changed".format("Empty"))

        def __delattr__(self, *args):
            raise AttributeError("Attributes of {0} object "
                                 "cannot be deleted".format("Empty"))

        def is_empty(self): return True
        def head(self): return None
        def last(self): return None
        def tail(self): return self
        def butlast(self): return self
        def push_front(self, v):
            return FingerTree.Single(self.measure, v)
        def push_back(self, v):
            return FingerTree.Single(self.measure, v)
        def __iter__(self): return iter([])

    class Single(object):
        __slots__ = ("measure", "elem",)

        def __init__(self, measure, elem):
            object.__setattr__(self, "measure", measure)
            object.__setattr__(self, "elem", elem)

        def __setattr__(self, *args):
            raise AttributeError("Attributes of {0} object "
                                 "cannot be changed".format("Single"))

        def __delattr__(self, *args):
            raise AttributeError("Attributes of {0} object "
                                 "cannot be deleted".format("Single"))

        def is_empty(self): return False
        def head(self): return self.elem
        def last(self): return self.elem
        def tail(self): return FingerTree.Empty(self.measure)
        def butlast(self): return FingerTree.Empty(self.measure)
        def push_front(self, v):
            return FingerTree.Deep(self.measure, [v], FingerTree.Empty(self.measure), [self.elem])
        def push_back(self, v):
            return FingerTree.Deep(self.measure, [self.elem], FingerTree.Empty(self.measure), [v])
        def __iter__(self): return iter([self.elem])

    class Deep(object):
        __slots__ = ("measure", "left", "middle", "right",)

        def __init__(self, measure, left, middle, right):
            object.__setattr__(self, "measure", measure)
            object.__setattr__(self, "left", left)
            object.__setattr__(self, "middle", middle)
            object.__setattr__(self, "right", right)

        def __setattr__(self, *args):
            raise AttributeError("Attributes of {0} object "
                                 "cannot be changed".format("Deep"))

        def __delattr__(self, *args):
            raise AttributeError("Attributes of {0} object "
                                 "cannot be deleted".format("Deep"))

        def is_empty(self): return False
        def head(self): return self.left[0]
        def last(self): return self.right[-1]

        def tail(self):
            if len(self.left) == 1:
                if self.middle.is_empty():
                    return FingerTree.from_iterable(self.measure, list(self.right))
                return FingerTree.Deep(self.measure,
                                       [self.middle.head()],
                                       self.middle.tail(),
                                       self.right)
            return FingerTree.Deep(self.measure, self.left[1:], self.middle, self.right)

        def butlast(self):
            if len(self.rigth) == 1:
                if self.middle.is_empty():
                    return FingerTree.from_iterable(self.measure, list(self.left))
                return FingerTree.Deep(self.measure,
                                       self.left,
                                       self.middle.butlast(),
                                       [self.middle.last()])
            return FingerTree.Deep(self.measure, self.left, self.middle, self.right[:-1])

        def push_front(self, v):
            if len(self.left) == 4:
                return FingerTree.Deep(self.measure,
                                       [v, self.left[0]],
                                       self.middle.push_front(Node3(*self.left[1:])),
                                       self.right)
            return FingerTree.Deep(self.measure, [v] + self.left, self.middle, self.right)

        def push_back(self, v):
            if len(self.right) == 4:
                return FingerTree.Deep(self.measure,
                                       self.left,
                                       self.middle.push_back(Node3(*self.right[:3])),
                                       [self.right[-1], v])                
            return FingerTree.Deep(self.measure, self.left, self.middle, self.right + [v])

        def __iter__(self):
            for l in self.left: yield l
            for m in self.middle:
                for mi in m:
                    yield mi
            for r in self.right: yield r

    @staticmethod
    def from_iterable(measure, it):
        tree = FingerTree.Empty(measure)
        return reduce(lambda acc, curr: acc.push_front(curr), it, tree)

    def __new__(_cls, measure):
        return FingerTree.Empty(measure)

#####################################################
# Possible applications of finger tree in practice
#####################################################

class Deque(object):
    def __new__(_cls):
        return FingerTree.Empty(lambda x: x)

    @staticmethod
    def from_iterable(it):
        return FingerTree.from_iterable(lambda x: x, it)
