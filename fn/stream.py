from sys import maxint, version
from itertools import chain

class Stream(object):

    __slots__ = ("_last", "_collection", "_origin")

    class _StreamIterator(object):
        
        __slots__ = ("_stream", "_position")

        def __init__(self, stream):
            self._stream = stream
            self._position = -1 # not started yet

        def __next__(self):
            # check if elements are available for next position
            # return next element or raise StopIteration
            self._position += 1
            if self._stream._fill_to(self._position):
                return self._stream._collection[self._position]

            raise StopIteration()

        if version.startswith("2"):
            next = __next__

    def __init__(self):
        self._collection = []
        self._last = -1 # not started yet
        self._origin = []

    def __lshift__(self, rvalue):
        iterator = rvalue() if callable(rvalue) else rvalue
        self._origin = chain(self._origin, iterator)
        return self

    def _fill_to(self, index):
        if self._last >= index:
            return True

        while self._last < index:
            try:
                n = next(self._origin)
            except StopIteration:
                return False

            self._last += 1
            self._collection.append(n)

        return True

    def __iter__(self):
        return Stream._StreamIterator(self)

    def __getitem__(self, index):
        if isinstance(index, int):
            # todo: i'm not sure what to do with negative indices
            if index < 0: raise TypeError, "Invalid argument type"
            self._fill_to(index)
        elif isinstance(index, slice):
            # todo: reimplement to work lazy
            low, high, step = index.indices(maxint)
            self._fill_to(max(low, high))
        else:
            raise TypeError, "Invalid argument type"

        return self._collection.__getitem__(index)
