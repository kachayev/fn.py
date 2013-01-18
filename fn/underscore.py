import operator
from .op import identity, curry, apply, flip
from .func import F

def fmap(f):    
    def applyier(self, other=None):
        if other is None:
            return self.__class__(F(self) << f)
        if isinstance(other, self.__class__):
            return self.__class__(lambda arg1: lambda arg2: f(self(arg1), other(arg2)))
        return self.__class__(F(flip(f), other) << F(self))
    return applyier

class _Callable(object):
    
    __slots__ = '_callback',

    def __init__(self, callback=identity):
        self._callback = callback

    def call(self, name, *args):
        """Call method from _ object by given name and arguments"""
        return self.__class__(F(apply) << operator.attrgetter(name) << F(self))

    def __getattr__(self, name):
        return self.__class__(F(operator.attrgetter(name)) << F(self))

    def __getitem__(self, k):
        if isinstance(k, self.__class__):
            return self.__class__(lambda arg1: lambda arg2: self(arg1)[k(arg2)])
        return self.__class__(F(operator.itemgetter(k)) << F(self))

    def __str__(self):
        """Build readable representation for function

        (_ < 7): (x1) => (x1 < 7)
        (_ + _*10): (x1, x2) => (x1 + x2*10)
        """
        raise NotImplementedError

    def __call__(self, *args):
        return curry(self._callback, *args)

    __add__ = fmap(operator.add)
    __mul__ = fmap(operator.mul)
    __sub__ = fmap(operator.sub)
    __mod__ = fmap(operator.mod)
    __pow__ = fmap(operator.pow)

    __and__ = fmap(operator.and_)
    __or__ = fmap(operator.or_)
    __xor__ = fmap(operator.xor)

    __div__ = fmap(operator.div)
    __divmod__ = fmap(divmod)
    __floordiv__ = fmap(operator.floordiv)
    __truediv__ = fmap(operator.truediv)

    __lshift__ = fmap(operator.lshift)
    __rshift__ = fmap(operator.rshift)

    __lt__ = fmap(operator.lt)
    __le__ = fmap(operator.le)
    __gt__ = fmap(operator.gt)
    __ge__ = fmap(operator.ge)
    __eq__ = fmap(operator.eq)
    __ne__ = fmap(operator.ne)

    __neg__ = fmap(operator.neg)
    __pos__ = fmap(operator.pos)
    __invert__ = fmap(operator.invert)

    __radd__ = fmap(flip(operator.add))
    __rmul__ = fmap(flip(operator.mul))
    __rsub__ = fmap(flip(operator.sub))
    __rmod__ = fmap(flip(operator.mod))
    __rpow__ = fmap(flip(operator.pow))
    __rdiv__ = fmap(flip(operator.div))
    __rdivmod__ = fmap(flip(divmod))
    __rtruediv__ = fmap(flip(operator.truediv))
    __rfloordiv__ = fmap(flip(operator.floordiv))

    __rlshift__ = fmap(flip(operator.lshift))
    __rrshift__ = fmap(flip(operator.rshift))

    __rand__ = fmap(flip(operator.and_))
    __ror__ = fmap(flip(operator.or_))
    __rxor__ = fmap(flip(operator.xor))

shortcut = _Callable()
