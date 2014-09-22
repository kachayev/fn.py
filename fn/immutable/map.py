

class Map(object):
    """
    Map is based on size balanced binary trees (or trees of bounded balance) as described by:

    - Stephen Adams, "Efficient sets: a balancing act", Journal of Functional Programming 3(4):553-562, October 1993, http://www.swiss.ai.mit.edu/~adams/BB/
    - J. Nievergelt and E.M. Reingold, "Binary search trees of bounded balance", SIAM journal of computing 2(1), March 1973

    Based on Haskell "containers" Data.Map: http://hackage.haskell.org/package/containers-0.5.5.1/docs/Data-Map.html
    """

    __slots__ = ("size", "balanceR", "balanceL", "delta", "ratio", "empty", "root", "null", "insert")

    delta = 3
    ratio = 2


    class _Bin(object):
        __slots__ = ("size", "key", "value", "left", "right")
        def __init__(self, size, key, value, left, right):
            self.size = size
            self.key = key
            self.value = value
            self.left = left
            self.right = right

        def __str__(self):
            return '("{}": {} - {} {})'.format(self.key, self.value, self.left, self.right)

        def __repr__(self):
            return str(self)


    class _Tip(object):
        def __nonzero__(self):
            return False

        def __str__(self):
            return "()"

        def __repr__(self):
            return str(self)


    def __init__(self, size=0, key=None, value=None, left=None, right=None):
        if size and key and value and left and right:
            self.root = self.__class__._Bin(size, key, value, left, right)
        else:
            self.root = self.__class__._Tip()


    def __str__(self):
        return str(self.root)


    def __repr__(self):
        return str(self)


    @classmethod
    def singleton(cls, key, value):
        return cls(1, key, value, cls.empty(), cls.empty())


    @classmethod
    def empty(cls):
        return cls()


    def null(self):
        return not bool(self.root)


    def size(self):
        if self.root:
            return self.root.size
        else:
            return 0


    def lookup(self, k):
        if self.null():
            return None
        else:
            r = self.root
            if k == r.key:
                return r.value
            elif k < r.key:
                return r.left.lookup(k)
            else:
                return r.right.lookup(k)


    def insert(self, kx, x):
        if self.null():
            return self.singleton(kx, x)
        else:
            r = self.root
            if kx < r.key:
                return self.balanceL(r.key, r.value, r.left.insert(kx, x), r.right)
            if kx > r.key:
                return self.balanceR(r.key, r.value, r.left, r.right.insert(kx, x))
            else:
                return Map(r.size, kx, x, r.left, r.right)


    @classmethod
    def balanceL(cls, k, x, l, r):
        if r.null():
            lr = l.root
            if l.null():
                return cls.singleton(k, x)
            elif lr.left.null() and lr.right.null():
                return Map(2, k, x, l, cls.empty())
            elif lr.left.null():
                lrr = lr.right.root
                return Map(3, lrr.key, lrr.value,
                        Map(1, lr.key, lr.value, cls.empty(), cls.empty()),
                        Map(1, k, x, cls.empty(), cls.empty()))
            elif lr.right.null():
                return Map(3, lr.key, lr.value, lr.left, Map(1, k, x, cls.empty(), cls.empty()))
            else:
                llr = lr.left.root
                lrr = lr.right.root
                if lrr.size < cls.ratio*llr.size:
                    return Map(1 + lr.size, lr.key, lr.value,
                            lr.left,
                            Map(1 + lrr.size, k, x, lr.right, cls.empty()))
                else:
                    return Map(1 + lr.size, lrr.key, lrr.value,
                            Map(1 + llr.size + lrr.left.size(), lr.key, lr.value, lr.left, lrr.left),
                            Map(1 + lr.right.size(), k, x, lrr.right, cls.empty()))

        else:
            rrs = r.root.size
            if l.null():
                return Map(1 + rrs, k, x, cls.empty(), r)
            else:
                lr = l.root
                if lr.size > cls.delta * rrs:
                    if lr.right.null() and lr.left.null():
                        raise Exception("Something went wrong in balanceL")
                    elif lr.right.root.size < cls.ratio * lr.left.root.size:
                        return Map(1 + lr.size + rrs, lr.key, lr.value,
                                lr.left,
                                Map(1 + rrs+ lr.right.root.size, k, x, lr.right, r))
                    else:
                        return Map(1 + lr.size + rrs, lr.right.root.key, lr.right.root.value,
                                Map(1 + lr.left.root.size + lr.right.root.left.size(), lr.key, lr.value, lr.left, lr.right.root.left),
                                Map(1 + rrs+ lr.right.root.right.size(), k, x, lr.right.root.right, r))
                else:
                    return Map(1 + lr.size, rrs, k, x, l, r)


    @classmethod
    def balanceR(cls, k, x, l, r):
        if l.null():
            rr = r.root
            if r.null():
                return cls.singleton(k, x)
            elif rr.left.null() and rr.right.null():
                return Map(2, k, x, cls.empty(), r)
            elif rr.left.null():
                return Map(3, rr.key, rr.value,
                        Map(1, k, x, cls.empty(), cls.empty()),
                        rr.right)
            elif rr.right.null():
                return Map(3, rr.left.root.key, rr.left.root.value,
                        Map(1, k, x, cls.empty(), cls.empty()),
                        Map(1, rr.key, rr.value, cls.empty(), cls.empty()))
            else:
                rrr = rr.right.root
                rlr = rr.left.root
                if rlr.size < cls.ratio * rrr.size:
                    return Map(1 + rr.size, rr.key, rr.value,
                            Map(1 + rlr.size, k, x, cls.empty(), rr.left),
                            rr.right)
                else:
                    return Map(1 + rr.size, rlr.key, rlr.value,
                            Map(1 + rlr.left.size(), k, x, cls.empty(), rlr.left),
                            Map(1 + rrr.size + rlr.right.size(), rr.key, rr.value, rlr.right, rr.right))

        else:
            lrs = l.root.size
            if r.null():
                return Map(1 + lrs, k, x, l, cls.empty())
            else:
                rr = r.root
                if rr.size > cls.delta * lrs:
                    if rr.left.null() and rr.right.null():
                        raise Exception("Something went wrong in balanceR")
                    elif rr.left.root.size < ratio * rr.right.root.size:
                        return Map(1 + lrs + rr.size, rr.key, rr.value,
                                Map(1 + lrs + rr.left.root.size, k, x, l, rr.left),
                                rr.right)
                    else:
                        return Map(1 + lrs + rr.size, rr.left.root.key, rr.left.root.value,
                                Map(1 + lrs + rr.left.root.left.size(), k, x, l, rr.left.root.left),
                                Map(1 + rr.right.root.size + rr.left.root.right.size(), rr.key, rr.value, rr.left.root.right, rr.right))
                else:
                    return Map(1 + lrs + rr.size, k, x, l, r)
