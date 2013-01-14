from itertools import islice, chain, izip, imap
from sys import version

# Syntax sugar to deal with Python 2/Python 3 
# differences: this one will return generator
# even in Python 2.*
map = imap if version.startswith("2") else map

def take(limit, base): 
    return islice(base, limit)

def drop(limit, base): 
    return islice(base, limit, None)

def nth(iterable, n, default=None):
    return next(islice(iterable, n, None), default)

def ncycles(iterable, n):
    return chain.from_iterable(repeat(tuple(iterable), n))

def flatten(listOfLists):
    return chain.from_iterable(listOfLists)

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)
