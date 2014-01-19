from fn.uniform import reduce

class Vector(object):
    """A vector is a collection of values indexed by contiguous integers.
    Based on Philip Bagwell's "Array Mapped Trie" and Rick Hickey's 
    "Bitmapped Vector Trie". As well as Clojure variant it supports access
    to items by index in log32N hops. 

    Usage:
    TBD
    """

    __slots__ = ("length", "shift", "root", "tail")

    class _Node(object):
        __slots__ = ("array")

        def __init__(self, values=None, init=None):
            self.array = values or [None]*32
            if init is not None: self.array[0] = init

        def __str__(self):
            return str(self.array)

    def __init__(self, length=0, shift=None, root=None, tail=None):
        self.length = length
        self.shift = shift if shift is not None else 5
        self.root = root or self.__class__._Node()
        self.tail = tail if tail is not None else []

    def assoc(self, pos, el):
        """Returns a new vector that contains el at given position.
        Note, that position must be <= len(vector)
        """
        if pos < 0 or pos > self.length: raise IndexError()
        if pos == self.length: return self.cons(el)
        if pos < self._tailoff():
            up = self.__class__._do_assoc(self.shift, self.root, pos, el)
            return self.__class__(self.length, self.shift, up, self.tail)

        up = self.tail[:]
        up[pos & 0x01f] = el;
        return self.__class__(self.length, self.shift, self.root, up)

    def _tailoff(self):
        if self.length < 32: return 0
        return ((self.length - 1) >> 5) << 5

    @classmethod
    def _do_assoc(cls, level, node, pos, el):
        r = cls._Node(node.array[:])
        if level == 0:
            r.array[pos & 0x01f] = el
        else:
            sub = (pos >> level) & 0x01f
            r.array[sub] = cls._do_assoc(level-5, node.array[sub], pos, el)
        return r

    def cons(self, el):
        # if there is a room in tail, just append value to tail
        if (self.length - self._tailoff()) < 32:
            tailup = self.tail[:]
            tailup.append(el)
            return self.__class__(self.length+1, self.shift, self.root, tailup)

        # if tail is already full, we need to push element into tree
        # (from the top)
        tailnode = self.__class__._Node(self.tail)

        # if root is overflowed, we need to expand the whole tree
        if (self.length >> 5) > (1 << self.shift):
            uproot = self.__class__._Node(init=self.root)
            uproot.array[1] = self.__class__._make_path(self.shift, tailnode)
            shift = self.shift + 5
        else:
            uproot = self._push_tail(self.shift, self.root, tailnode)
            shift = self.shift

        return self.__class__(self.length+1, shift, uproot, [el])

    def _push_tail(self, level, root, tail):
        sub = ((self.length - 1) >> level) & 0x01f
        r = self.__class__._Node(root.array[:])
        if level == 5:
            r.array[sub] = tail
        else:
            child = root.array[sub]
            if child is not None:
                r.array[sub] = self._push_tail(level-5, child, tail)
            else:
                r.array[sub] = self.__class__._make_path(level-5, tail)
        return r

    @classmethod
    def _make_path(cls, level, node):
        if level == 0: return node
        return cls._Node(init=cls._make_path(level-5, node))

    def get(self, pos):
        """Returns a value accossiated with position"""
        if pos < 0 or pos > self.length: raise IndexError()
        if pos >= self._tailoff(): return self.tail[pos & 0x01f]
        bottom = reduce(lambda node, level: node.array[(pos >> level) & 0x01f],
                        range(self.shift,0,-5), self.root)
        return bottom.array[pos & 0x01f]

    def peek(self):
        """Returns the last item in vector or None if vector is empty"""
        pass

    def pop(self):
        """Returns a new vector without the last item"""
        pass
    
    def subvec(self, start, end=None):
        """Returns a new vector of the items in vector from start to end"""
        pass

    def __len__(self):
        return self.length

    def __iter__(self):
        pass

    def __getitem__(self, pos):
        return self.get(pos)

    def __setitem__(self, pos, val):
        raise NotImplementedError()
    
