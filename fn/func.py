from functools import partial

from .op import identity, flip

class F(object):

    __slots__ = "f", 

    def __init__(self, f = identity, *args, **kwargs):
        self.f = partial(f, *args, **kwargs) if any([args, kwargs]) else f

    @classmethod
    def __compose(cls, f, g):
        return cls(lambda *args, **kwargs: f(g(*args, **kwargs)))

    def __ensure_callable(self, f):
        return self.__class__(*f) if isinstance(f, tuple) else f        

    def __rshift__(self, g):
        return self.__class__.__compose(self.__ensure_callable(g), self.f)

    def __lshift__(self, g):
        return self.__class__.__compose(self.f, self.__ensure_callable(g))

    def  __call__(self, *args, **kwargs):
        return self.f(*args, **kwargs)