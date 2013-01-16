from functools import partial

from .op import identity

class F(object):

    def __init__(self, f = identity, *args, **kwargs):
        self.f = partial(f, *args, **kwargs) if any([args, kwargs]) else f

    def __lshift__(self, g):
        return self.__class__(lambda *args, **kwargs: self.f(g(*args, **kwargs)))

    def  __call__(self, *args, **kwargs):
        return self.f(*args, **kwargs)