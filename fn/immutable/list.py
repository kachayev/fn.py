from fn.op import foldr
from fn.uniform import reduce

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
        return self.__class__(el, self)

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

    def __bool__(self):
        return len(self) > 0

    @staticmethod
    def from_iterable(it):
        ''' iterable -> LinkedList

        produces LinkedList with the contents of the consumed iterable
        '''
        return foldr(lambda x, y: y.cons(x), LinkedList())(tuple(it))


class Stack(LinkedList):
    """Technically it's a LinkedList, but it provides more familiar
    API for Stack operations: push and pop. It also distinguishes between
    empty and non-empty structure, so trying to pop from empty stack will
    throw ValueError.
    """

    def push(self, el):
        return self.cons(el)

    def pop(self):
        if not self: raise ValueError("Stack is empty")
        return self.head, self.tail

    def is_empty(self):
        return not self

class Queue(object):
    """A queue is a particular kind of collection in which the entities in the collection
    are kept in order and the principal operations on the collection are the addition of
    entities to the rear terminal position, known as enqueue, and removal of entities from
    the front terminal position, known as dequeue.

    Queue data structure description on Wikipedia:
    [1] http://en.wikipedia.org/wiki/Queue_(abstract_data_type)

    Implementation based on two linked lists (left and right). Enqueue operation
    performs cons on right list (the end of the queue). Dequeue peeks first element
    from the left list (when possible), if left list is emptpy we populate left list
    with element from right one-by-one (in natural reverse order). Complexity of both
    operations are O(1).

    Such implementation is also known as "Banker's Queue" in different papers,
    i.e. in Chris Okasaki, "Purely Functional Data Structures"

    Usage:

    >>> from fn.immutable import Queue
    >>> q = Queue()
    >>> q1 = q.enqueue(10)
    >>> q2 = q1.enqueue(20)
    >>> el, tail = q2.dequeue()
    >>> el
    10
    >>> tail.dequeue()
    (20, <fn.immutable.list.Queue object at 0x1055554d0>)
    """

    __slots__ = ("left", "right")

    def __init__(self, left=None, right=None):
        self.left = left if left is not None else LinkedList()
        self.right = right if right is not None else LinkedList()

    def enqueue(self, el):
        """Returns new queue object with given element is added onto the end"""
        # check if we need to rebalance to prevent spikes
        if len(self.left) >= len(self.right):
            return Queue(self.left, self.right.cons(el))
        left = reduce(lambda acc, el: acc.cons(el), self.right, self.left)
        return Queue(left, LinkedList().cons(el))

    def dequeue(self):
        """Return pair of values: the item from the front of the queue and
        the new queue object without poped element.
        """
        if not self: raise ValueError("Queue is empty")
        # if there is at least one element on the left, we can return it
        if self.left:
            return self.left.head, Queue(self.left.tail, self.right)

        # in other case we need to copy right to left before
        d = reduce(lambda acc, el: acc.cons(el), self.right, LinkedList())
        return d.head, Queue(d.tail, LinkedList())

    def is_empty(self):
        return len(self) == 0

    def __iter__(self):
        curr = self
        while curr:
            el, curr = curr.dequeue()
            yield el

    def __nonzero__(self):
        return len(self)

    def __bool__(self):
        return len(self) > 0

    def __len__(self):
        lleft = len(self.left) if self.left is not None else 0
        lright = len(self.right) if self.right is not None else 0
        return lleft + lright

class Deque(object):
    """Double-ended queue is an  abstract data type that generalizes
    a queue, for which elements can be added to or removed from either
    the front (head) or back (tail).

    More information on Wikipedia:
    [1] http://en.wikipedia.org/wiki/Double-ended_queue

    Implementation details are described here:
    "Confluently Persistent Deques via Data Structural Bootstrapping"
    [2] https://cs.uwaterloo.ca/~imunro/cs840/p155-buchsbaum.pdf

    xxx: TBD
    """
    pass
