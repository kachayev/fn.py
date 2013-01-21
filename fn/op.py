from sys import version

identity = lambda arg: arg
apply = apply if version.startswith("2") else _apply

def _apply(f, args, kwargs=None):
    return f(*args, **(kwargs or {}))

def flip(f):
    """Return function that will apply arguments in reverse order"""

    # Original function is saved in special attribute
    # in order to optimize operation of "duble flipping",
    # so flip(flip(a)) is a
    flipper = getattr(f, "__flipback__", None)
    if flipper is not None:
        return flipper

    def _flipper(a, b):
        return f(b, a)

    _flipper.__flipback__ = f
    return _flipper

def curry(f, arg, *rest):
    return curry(f(arg), *rest) if rest else f(arg)

from .func import F
from itertools import starmap

def zipwith(f): 
    'zipwith(f)(seq1, seq2, ..) -> [f(seq1[0], seq2[0], ..), f(seq1[1], seq2[1], ..), ...]'
    return F(starmap, f) << zip
