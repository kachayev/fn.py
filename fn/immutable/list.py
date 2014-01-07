class LinkedList(object):
    """Represents simplest singly linked list. Doesn't distinguish
    between empty and not-empty list (taking head of empty list will
    return None as a result).

    More about Linked List data structure on Wikipedia:
    [1] http://en.wikipedia.org/wiki/Linked_list

    Usage:

    >>> from fn.immutable import LinkedList
    >>> l = LinkedList()
    >>> l.cons(10)
    <fn.immutable.list.LinkedList object at 0x10acfbb00>
    >>> l.cons(10).cons(20).cons(30).head
    30
    >>> l.cons(10).cons(20).cons(30).tail
    <fn.immutable.list.LinkedList object at 0x10acfbc20>
    >>> l.cons(10).cons(20).cons(30).tail.head
    20
    >>> len(l.cons(10).cons(20).cons(30))
    3
    >>> list(l.cons(10).cons(20).cons(30))
    [30, 20, 10]
    >>> list(l + 100 + 110 + 120)
    [120, 110, 100]
    """

    __slots__ = ("head", "tail", "_count")
    
    def __init__(self, head=None, tail=None):
        self.head = head
        self.tail = tail
        self._count = 0 if tail is None else (len(tail) + 1)

    def cons(self, el):
        return LinkedList(el, self)

    def __add__(self, el):
        return self.cons(el)

    def __radd__(self, el):
        return self.cons(el)

    def __iter__(self):
        l = self
        while l:
            yield l.head
            l = l.tail

    def __len__(self):
        return self._count

    def __nonzero__(self):
        return self.tail is not None

class Stack(object):
    pass

class Deque(object):
    pass
