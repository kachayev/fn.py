import operator
from itertools import repeat, count

from .op import identity, curry, apply, flip
from .iters import map, zip
from .func import F
from sys import version_info

div = operator.div if version_info.major == 2 else operator.truediv

def fmap(f, format=""):
    def applyier(self, other=None):
        fmt = "(%s)" % format.replace("self", self._format)
        if other is None:
            return self.__class__(F(self) << f, fmt)
        elif isinstance(other, self.__class__):
            call = lambda arg1: lambda arg2: f(self(arg1), other(arg2))
            return self.__class__(call, fmt.replace("other", other._format))
        else:
            call = F(flip(f), other) << F(self)
            return self.__class__(call, fmt.replace("other", str(other)))
    return applyier

class _Callable(object):
    
    __slots__ = '_callback', "_format"

    def __init__(self, callback=identity, format="_"):
        self._callback = callback
        self._format = format

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
        (_ + _*10): (x1, x2) => (x1 + (x2*10))
        """
        # args iterator with produce infinite sequence
        # args -> (x1, x2, x3, ...) 
        args = map("".join, zip(repeat("x"), map(str, count(1))))
        l, r = [], self._format
        # replace all "_" signs from left to right side 
        while r.count("_"):
            n = next(args)
            r = r.replace("_", n, 1)
            l.append(n)

        return "({left}) => {right}".format(left=", ".join(l), right=r)

    def __call__(self, *args):
        return curry(self._callback, *args)

    __add__ = fmap(operator.add, "self + other")
    __mul__ = fmap(operator.mul, "self * other")
    __sub__ = fmap(operator.sub, "self - other")
    __mod__ = fmap(operator.mod, "self % other")
    __pow__ = fmap(operator.pow, "self ** other")

    __and__ = fmap(operator.and_, "self & other")
    __or__ = fmap(operator.or_, "self | other")
    __xor__ = fmap(operator.xor, "self ^ other")

    __div__ = fmap(div, "self / other")
    __divmod__ = fmap(divmod, "self / other")
    __floordiv__ = fmap(operator.floordiv, "self / other")
    __truediv__ = fmap(operator.truediv, "self / other")

    __lshift__ = fmap(operator.lshift, "self << other")
    __rshift__ = fmap(operator.rshift, "self >> other")

    __lt__ = fmap(operator.lt, "self < other")
    __le__ = fmap(operator.le, "self <= other")
    __gt__ = fmap(operator.gt, "self > other")
    __ge__ = fmap(operator.ge, "self >= other")
    __eq__ = fmap(operator.eq, "self == other")
    __ne__ = fmap(operator.ne, "self != other")

    __neg__ = fmap(operator.neg, "-self")
    __pos__ = fmap(operator.pos, "+self")
    __invert__ = fmap(operator.invert, "~self")

    __radd__ = fmap(flip(operator.add), "other + self")
    __rmul__ = fmap(flip(operator.mul), "other * self")
    __rsub__ = fmap(flip(operator.sub), "other - self")
    __rmod__ = fmap(flip(operator.mod), "other % self")
    __rpow__ = fmap(flip(operator.pow), "other ** self")
    __rdiv__ = fmap(flip(div), "other / self")
    __rdivmod__ = fmap(flip(divmod), "other / self")
    __rtruediv__ = fmap(flip(operator.truediv), "other / self")
    __rfloordiv__ = fmap(flip(operator.floordiv), "other / self")

    __rlshift__ = fmap(flip(operator.lshift), "other << self")
    __rrshift__ = fmap(flip(operator.rshift), "other >> self")

    __rand__ = fmap(flip(operator.and_), "other & self")
    __ror__ = fmap(flip(operator.or_), "other | self")
    __rxor__ = fmap(flip(operator.xor), "other ^ self")

shortcut = _Callable()
