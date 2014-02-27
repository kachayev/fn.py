from sys import version_info
from collections import deque, Iterable
from operator import add, itemgetter, attrgetter, not_
from functools import partial
from itertools import (islice, 
                       chain,                        
                       starmap, 
                       repeat, 
                       tee, 
                       cycle,
                       takewhile, 
                       dropwhile,
                       combinations)

from .op import flip
from .func import F
from .underscore import shortcut as _
from .uniform import *

def take(limit, base): 
    return islice(base, limit)

def drop(limit, base): 
    return islice(base, limit, None)

def takelast(n, iterable):
    "Return iterator to produce last n items from origin"
    return iter(deque(iterable, maxlen=n))

def droplast(n, iterable):
    "Return iterator to produce items from origin except last n"
    t1, t2 = tee(iterable)
    return map(itemgetter(0), zip(t1, islice(t2, n, None)))

def consume(iterator, n=None):
    """Advance the iterator n-steps ahead. If n is none, consume entirely.

    http://docs.python.org/3.4/library/itertools.html#itertools-recipes
    """
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(islice(iterator, n, n), None)

def nth(iterable, n, default=None):
    """Returns the nth item or a default value

    http://docs.python.org/3.4/library/itertools.html#itertools-recipes
    """
    return next(islice(iterable, n, None), default)

# widely-spreaded shortcuts to get first item, all but first item,
# second item, and first item of first item from iterator respectively
head = first = partial(flip(nth), 0)
tail = rest = partial(drop, 1)
second = F(rest) >> first
ffirst = F(first) >> first

# shortcut to remove all falsey items from iterable
compact = partial(filter, None)

def reject(func, iterable):
    """Return an iterator yielding those items of iterable for which func(item)
    is false. If func is None, return the items that are false.
    """
    return filter(F(not_) << (func or _), iterable)

def iterate(f, x):
    """Return an iterator yielding x, f(x), f(f(x)) etc.
    """
    while True:
        yield x
        x = f(x)

def padnone(iterable):
    """Returns the sequence elements and then returns None indefinitely.
    Useful for emulating the behavior of the built-in map() function.

    http://docs.python.org/3.4/library/itertools.html#itertools-recipes
    """
    return chain(iterable, repeat(None))

def ncycles(iterable, n):
    """Returns the sequence elements n times

    http://docs.python.org/3.4/library/itertools.html#itertools-recipes
    """
    return chain.from_iterable(repeat(tuple(iterable), n))

def repeatfunc(func, times=None, *args):
    """Repeat calls to func with specified arguments.
    Example:  repeatfunc(random.random)

    http://docs.python.org/3.4/library/itertools.html#itertools-recipes
    """
    if times is None:
        return starmap(func, repeat(args))
    return starmap(func, repeat(args, times))

def grouper(n, iterable, fillvalue=None):
    """Collect data into fixed-length chunks or blocks, so
    grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx

    http://docs.python.org/3.4/library/itertools.html#itertools-recipes
    """
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

def group_by(keyfunc, iterable):
    """Returns a dict of the elements from given iterable keyed by result
    of keyfunc on each element. The value at each key will be a list of
    the corresponding elements, in the order they appeared in the iterable.
    """
    grouped = {}
    for item in iterable:
        grouped.setdefault(keyfunc(item), []).append(item)
    return grouped

def roundrobin(*iterables):
    """roundrobin('ABC', 'D', 'EF') --> A D E B F C
    Recipe originally credited to George Sakkis.
    Reimplemented to work both in Python 2+ and 3+. 

    http://docs.python.org/3.4/library/itertools.html#itertools-recipes
    """
    pending = len(iterables)
    next_attr = "next" if version_info[0] == 2 else "__next__"
    nexts = cycle(map(attrgetter(next_attr), map(iter, iterables)))
    while pending:
        try:
            for n in nexts:
                yield n()
        except StopIteration:
            pending -= 1
            nexts = cycle(islice(nexts, pending))

def partition(pred, iterable):
    """Use a predicate to partition entries into false entries and true entries
    partition(is_odd, range(10)) --> 0 2 4 6 8   and  1 3 5 7 9

    http://docs.python.org/3.4/library/itertools.html#itertools-recipes
    """
    t1, t2 = tee(iterable)
    return filterfalse(pred, t1), filter(pred, t2)

def splitat(t, iterable):
    """Split iterable into two iterators after given number of iterations
    splitat(2, range(5)) --> 0 1 and 2 3 4
    """
    t1, t2 = tee(iterable)
    return islice(t1, t), islice(t2, t, None)

def splitby(pred, iterable):
    """Split iterable into two iterators at first false predicate
    splitby(is_even, range(5)) --> 0 and 1 2 3 4
    """
    t1, t2 = tee(iterable)
    return takewhile(pred, t1), dropwhile(pred, t2)

def powerset(iterable):
    """powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)

    http://docs.python.org/3.4/library/itertools.html#itertools-recipes
    """
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def pairwise(iterable):
    """pairwise(s) -> (s0,s1), (s1,s2), (s2, s3), ...

    http://docs.python.org/3.4/library/itertools.html#itertools-recipes
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def iter_except(func, exception, first_=None):
    """ Call a function repeatedly until an exception is raised.

    Converts a call-until-exception interface to an iterator interface.
    Like __builtin__.iter(func, sentinel) but uses an exception instead
    of a sentinel to end the loop.

    Examples:
        iter_except(functools.partial(heappop, h), IndexError)   # priority queue iterator
        iter_except(d.popitem, KeyError)                         # non-blocking dict iterator
        iter_except(d.popleft, IndexError)                       # non-blocking deque iterator
        iter_except(q.get_nowait, Queue.Empty)                   # loop over a producer Queue
        iter_except(s.pop, KeyError)                             # non-blocking set iterator

    http://docs.python.org/3.4/library/itertools.html#itertools-recipes
    """
    try:
        if first_ is not None:
            yield first_()            # For database APIs needing an initial cast to db.first()
        while 1:
            yield func()
    except exception:
        pass


def flatten(items):
    """Flatten any level of nested iterables (not including strings, bytes or
    bytearrays).
    Reimplemented to work with all nested levels (not only one).

    http://docs.python.org/3.4/library/itertools.html#itertools-recipes
    """
    for item in items:
        is_iterable = isinstance(item, Iterable)
        is_string_or_bytes = isinstance(item, (str, bytes, bytearray))
        if is_iterable and not is_string_or_bytes:
            for i in flatten(item):
                yield i
        else:
            yield item

if version_info[0] == 3 and version_info[1] >= 3:
    from itertools import accumulate
else:
    def accumulate(iterable, func=add):
        """Make an iterator that returns accumulated sums. 
        Elements may be any addable type including Decimal or Fraction. 
        If the optional func argument is supplied, it should be a 
        function of two arguments and it will be used instead of addition.

        Origin implementation:
        http://docs.python.org/dev/library/itertools.html#itertools.accumulate

        Backported to work with all python versions (< 3.3)
        """
        it = iter(iterable)
        total = next(it)
        yield total
        for element in it:
            total = func(total, element)
            yield total

