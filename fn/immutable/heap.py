from functools import partial
from fn.op import identity

default_cmp = (lambda a,b: -1 if (a < b) else 1)

class _MergeBased(object):

    def __nonzero__(self):
        return self.root is not None

    def __bool__(self):
        return self.__nonzero__()

    def __iter__(self):
        """Extract elements one-by-one.
        Note, that list(*Heap()) gives you sorted list as result.
        """
        curr = self
        while curr:
            r, curr = curr.extract()
            yield r

    def __lt__(self, other):
        if (not self) and (not other): return False
        if not self: return True
        if not other: return False
        return self.cmpfn(self.keyfn(self.root), self.keyfn(other.root)) < 0

class SkewHeap(_MergeBased):
    """A skew heap (or self-adjusting heap) is a heap data structure
    implemented as a binary-tree. Amortized complexity analytics can
    be used to demonstrate that all operations one a skew heap can be
    done in O(log n).

    Skew heaps may be described with the following recursive definition:
    * a heap with only one element is a skew heap
    * the result of skew merging two skew heaps is also a skew heap

    In Haskell type definition it should looks like following:
    data Skew a = Empty | Node a (Skew a) (Skew a)

    More information on Wikipedia:
    [1] http://en.wikipedia.org/wiki/Skew_heap

    One can also check slides from my KyivPy#11 talk "Union-based heaps":
    [2] http://goo.gl/VMgdG2

    Basic usage sample:

    >>> from fn.immutable import SkewHeap
    >>> s = SkewHeap(10)
    >>> s = s.insert(20)
    >>> s
    <fn.immutable.heap.SkewHeap object at 0x10b14c050>
    >>> s = s.insert(30)
    >>> s
    <fn.immutable.heap.SkewHeap object at 0x10b14c158> # <-- other object
    >>> s.extract()
    (10, <fn.immutable.heap.SkewHeap object at 0x10b14c050>)
    >>> _, s = s.extract()
    >>> s.extract()
    (20, <fn.immutable.heap.SkewHeap object at 0x10b14c1b0>)
    """

    __slots__ = ("root", "left", "right", "keyfn", "cmpfn", "_make_heap")

    def __init__(self, el=None, left=None, right=None, key=None, cmp=None):
        """Creates skew heap with one element (or empty one)"""
        self.root = el
        self.left = left
        self.right = right
        self.keyfn = key or identity
        self.cmpfn = cmp or default_cmp
        self._make_heap = partial(self.__class__, key=self.keyfn, cmp=self.cmpfn)        

    def insert(self, el):
        """Returns new skew heap with additional element"""
        return self._make_heap(el).union(self)

    def extract(self):
        """Returns pair of values:
        * minimum (or maximum regarding to given compare function)
        * new skew heap without extracted element

        Or None and empty heap if self is an empty heap.
        """
        if not self: return None, self._make_heap()
        return self.root, self.left.union(self.right) if self.left else self._make_heap()

    def union(self, other):
        """Merge two heaps and returns new one (skew merging)"""
        if not self: return other
        if not other: return self

        if self < other:
            return self._make_heap(self.root, other.union(self.right), self.left)
        return self._make_heap(other.root, self.union(other.right), other.left)

class PairingHeap(_MergeBased):
    """A pairing heap is either an empty heap, or a pair consisting of a root
    element and a possibly empty list of pairing heap. The heap ordering property
    requires that all the root elements of the subheaps in the list are not
    smaller (bigger) than the root element of the heap.

    In Haskell type definition it should looks like following:
    data Pairing a = Empty | Node a [Pairing a]

    Pairing heap has and excellent practical amortized performance. The amortized
    time per extract is less than O(log n), find-min/find-max, merge and insert are O(1).

    More information about performance bounds you can find here:
    "The Pairing Heap: A New Form of Self-Adjusting Heap"
    [1] http://www.cs.cmu.edu/afs/cs.cmu.edu/user/sleator/www/papers/pairing-heaps.pdf

    More general information on Wikipedia:
    [2] http://en.wikipedia.org/wiki/Pairing_heap

    One can also check slides from my KyivPy#11 talk "Union-based heaps":
    [3] http://goo.gl/VMgdG2

    Basic usage sample:

    >>> from fn.immutable import PairingHeap
    >>> ph = PairingHeap("a")
    >>> ph = ph.insert("b")
    >>> ph
    <fn.immutable.heap.PairingHeap object at 0x10b13fa00>
    >>> ph = ph.insert("c")
    >>> ph
    <fn.immutable.heap.PairingHeap object at 0x10b13fa50>
    >>> ph.extract()
    ('a', <fn.immutable.heap.PairingHeap object at 0x10b13fa00>)
    >>> _, ph = ph.extract()
    >>> ph.extract()
    ('b', <fn.immutable.heap.PairingHeap object at 0x10b13f9b0>)
    """

    __slots__ = ("root", "subs", "keyfn", "cmpfn", "_make_heap")

    def __init__(self, el=None, subs=None, key=None, cmp=None):
        """Creates singlton from given element 
        (pairing heap with one element or empty one)
        """
        self.root = el
        self.subs = subs
        self.keyfn = key or identity
        self.cmpfn = cmp or default_cmp
        self._make_heap = partial(self.__class__, key=self.keyfn, cmp=self.cmpfn)

    def insert(self, el):
        """Returns new pairing heap with additional element"""
        return self.union(self._make_heap(el))

    def extract(self):
        """Returns pair of values:
        * minimum (or maximum regarding to given compare function)
        * new pairing heap without extracted element

        Or None and empty heap if self is an empty heap.
        """
        if not self: return None, self._make_heap()
        return self.root, PairingHeap._pairing(self._make_heap, self.subs)

    def union(self, other):
        """Returns new heap as a result of merging two given
        
        Note, that originally this operation for pairingi heap was
        named "meld", see [1] and [2]. We use here name "union" to
        follow consistent naming convention for all heap implementations.
        """ 
        if not self: return other
        if not other: return self

        if self < other:
            return self._make_heap(self.root, (other, self.subs))
        return self._make_heap(other.root, (self, other.subs))

    @staticmethod
    def _pairing(heap, hs):
        if hs is None: return heap()
        (h1, tail) = hs
        if tail is None: return h1
        (h2, tail) = tail
        return PairingHeap._pairing(heap, (h1.union(h2), tail))
