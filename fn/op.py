from sys import version_info

identity = lambda arg: arg

def _apply(f, args=None, kwargs=None):
    return f(*(args or []), **(kwargs or {}))

apply = apply if version_info[0] == 2 else _apply

def call(f, *args, **kwargs):
    return f(*args, **kwargs)

def flip(f):
    """Return function that will apply arguments in reverse order"""

    # Original function is saved in special attribute
    # in order to optimize operation of "duble flipping",
    # so flip(flip(A)) is A
    # Do not use this approach for underscore callable, 
    # see https://github.com/kachayev/fn.py/issues/23
    flipper = getattr(f, "__flipback__", None)
    if flipper is not None:
        return flipper

    def _flipper(a, b): 
        return f(b, a)
    
    setattr(_flipper, "__flipback__", f)
    return _flipper

def curry(f, arg, *rest):
    return curry(f(arg), *rest) if rest else f(arg)

from .func import F
from .uniform import * 
from itertools import starmap

def zipwith(f): 
    'zipwith(f)(seq1, seq2, ..) -> [f(seq1[0], seq2[0], ..), f(seq1[1], seq2[1], ..), ...]'
    return F(starmap, f) << zip

def foldl(f, init=None):
    """Return function to fold iterator to scala value 
    using passed function as reducer.

    Usage:
    >>> print foldl(_ + _)([0,1,2,3,4])
    10
    >>> print foldl(_ * _, 1)([1,2,3])
    6
    """
    def fold(it): 
        args = [f, it]
        if init is not None: args.append(init)
        return reduce(*args)

    return fold

def foldr(f, init=None):
    """Return function to fold iterator to scala value using 
    passed function as reducer in reverse order (consume values 
    from iterator from right-to-left).

    Usage:
    >>> print foldr(call, 10)([lambda s: s**2, lambda k: k+10])
    400
    """
    def fold(it): 
        args = [flip(f), reversed(it)]
        if init is not None: args.append(init)
        return reduce(*args)

    return fold

def unfold(f):
    """Return function to unfold value into stream using 
    passed function as values producer. Passed function should 
    accept current cursor and should return: 
      * tuple of two elements (value, cursor), value will be added 
        to output, cursor will be used for next function call 
      * None in order to stop producing sequence 

    Usage:
    >>> doubler = unfold(lambda x: (x*2, x*2))
    >>> list(islice(doubler(10), 0, 10))
    [20, 40, 80, 160, 320, 640, 1280, 2560, 5120, 10240]
    """
    def _unfolder(start):
        value, curr = None, start
        while 1:
            step = f(curr)
            if step is None: break
            value, curr = step
            yield value
    return _unfolder
