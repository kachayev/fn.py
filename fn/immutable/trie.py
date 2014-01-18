class Vector(object):
    """A vector is a collection of values indexed by contiguous integers.
    Based on Philip Bagwell's "Array Mapped Trie" and Rick Hickey's 
    "Bitmapped Vector Trie". As well as Clojure variant it supports access
    to items by index in log32N hops. 

    Usage:
    TBD
    """

    def assoc(self, pos, el):
        """Returns a new vector that contains el at given position.
        Note, that position must be <= len(vector)
        """
        pass
    
    def get(self, pos):
        """Returns a value accossiated with position"""
        pass

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
        pass

    def __iter__(self):
        pass

    def __getitem__(self, pos):
        pass

    def __setitem__(self, pos, val):
        raise NotImplementedError()
    
