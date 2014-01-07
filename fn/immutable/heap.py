class _MergeBased(object):

    def __nonzero__(self):
        return self.root is not None

    def __iter__(self):
        """Extract elements one-by-one.
        Note, that list(*Heap()) gives you sorted list as result.
        """
        curr = self
        while curr:
            r, curr = curr.extract()
            yield r    

class SkewHeap(_MergeBased):
    """A skew heap (or self-adjusting heap) is a heap data structure
    implemented as a binary-tree. Amortized complexity analytics can
    be used to demonstrate that all operations one a skew heap can be
    done in O(log n).

    Skew heaps may be described with the following recursive definition:
    * a heap with only one element is a skew heap
    * the result of skew merging two skew heaps is also a skew heap

    More information: http://en.wikipedia.org/wiki/Skew_heap
    """

    __slots__ = ("root", "left", "right")

    def __init__(self, el=None, left=None, right=None):
        """Creates skew heap with one element (or empty one)"""
        self.root = el
        self.left = left
        self.right = right

    def insert(self, el):
        """Returns new skew heap with additional element"""
        return SkewHeap(el).union(self)

    def extract(self):
        """Returns pair of values:
        * minimum (or maximum regarding to given compare function)
        * new skew heap without extracted element

        Or None and empty heap if self is an empty heap.
        """
        if not self: return None, SkewHeap()
        return self.root, self.left.union(self.right) if self.left else SkewHeap()

    def union(self, other):
        """Merge two heaps and returns new one (skew merging)"""
        if not self: return other
        if not other: return self

        # xxx: custom compare function
        if self.root < other.root:
            return SkewHeap(self.root, other.union(self.right), self.left)
        return SkewHeap(other.root, self.union(other.right), other.left)

class PairingHeap(_MergeBased):
    """A pairing heap is either an empty heap, or a pair consisting of a root
    element and a possibly empty list of pairing heap. The heap ordering property
    requires that all the root elements of the subheaps in the list are not
    smaller (bigger) than the root element of the heap.

    In Haskell-like type definition it should looks like following:
    type PairingHeap[Elem] = Empty | Heap(elem: Elem, subheaps: List[PairingHeap[Elem]])

    Pairing heap has and excellent practical amortized performance. The amortized
    time per extract is less than O(log n), find-min/find-max, merge and insert are O(1).
    More information about performance bounds you can find here:

    [1] "The Pairing Heap: A New Form of Self-Adjusting Heap"
    (http://www.cs.cmu.edu/afs/cs.cmu.edu/user/sleator/www/papers/pairing-heaps.pdf)

    More general information on Wikipedia:
    [2] http://en.wikipedia.org/wiki/Pairing_heap
    """

    __slots__ = ("root", "subs")

    def __init__(self, el=None, subs=None):
        """Creates singlton from given element 
        (pairing heap with one element or empty one)
        """
        self.root = el
        self.subs = subs

    def insert(self, el):
        """Returns new pairing heap with additional element"""
        return self.union(PairingHeap(el))

    def extract(self):
        """Returns pair of values:
        * minimum (or maximum regarding to given compare function)
        * new pairing heap without extracted element

        Or None and empty heap if self is an empty heap.
        """
        if not self: return None, SkewHeap()
        return self.root, PairingHeap._pairing(self.subs)

    def union(self, other):
        """Returns new heap as a result of merging two given
        
        Note, that originally this operation for pairingi heap was
        named "meld", see [1] and [2]. We use here name "union" to
        follow consistent naming convention for all heap implementations.
        """ 
        if not self: return other
        if not other: return self

        # xxx: custom compare function
        if self.root < other.root:
            return PairingHeap(self.root, (other, self.subs))
        return PairingHeap(other.root, (self, other.subs))

    @classmethod
    def _pairing(cls, hs):
        if hs is None: return cls()
        (h1, tail) = hs
        if tail is None: return h1
        (h2, tail) = tail
        return cls._pairing((h1.union(h2), tail))
