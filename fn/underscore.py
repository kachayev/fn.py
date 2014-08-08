import re
import operator
import string
import random

from sys import version_info
from itertools import repeat, count

from .op import identity, apply, flip
from .uniform import map, zip
from .func import F

div = operator.div if version_info[0] == 2 else operator.truediv

letters = string.letters if version_info[0] == 2 else string.ascii_letters

def _random_name():
    return "".join(random.choice(letters) for _ in range(14))

def fmap(f, format):
    def applyier(self, other):
        fmt = "(%s)" % format.replace("self", self._format)

        if isinstance(other, self.__class__):
            return self.__class__((f, self, other),
                                  fmt.replace("other", other._format),
                                  dict(list(self._format_args.items()) + list(other._format_args.items())),
                                  self._arity + other._arity)
        else:
            call = F(flip(f), other) << F(self)
            name = _random_name()
            return self.__class__(call,
                                  fmt.replace("other", "%%(%s)r" % name),
                                  dict(list(self._format_args.items()) + [(name, other)]),
                                  self._arity)
    return applyier

class ArityError(TypeError):
    def __str__(self):
        return "{0!r} expected {1} arguments, got {2}".format(*self.args)

def unary_fmap(f, format):
    def applyier(self):
        fmt = "(%s)" % format.replace("self", self._format)
        return self.__class__(F(self) << f, fmt, self._format_args, self._arity)
    return applyier

class _Callable(object):

    __slots__ = "_callback", "_format", "_format_args", "_arity"
    # Do not use "flipback" approach for underscore callable,
    # see https://github.com/kachayev/fn.py/issues/23
    __flipback__ = None

    def __init__(self, callback=identity, format="_", format_args=None, arity=1):
        self._callback = callback
        self._format = format
        self._format_args = format_args or {}
        self._arity = arity

    def call(self, name, *args, **kwargs):
        """Call method from _ object by given name and arguments"""
        return self.__class__(F(lambda f: apply(f, args, kwargs)) << operator.attrgetter(name) << F(self))

    def __getattr__(self, name):
        attr_name = _random_name()
        return self.__class__(F(operator.attrgetter(name)) << F(self),
                              "getattr(%s, %%(%s)r)" % (self._format, attr_name),
                              dict(list(self._format_args.items()) + [(attr_name,name)]),
                              self._arity)

    def __getitem__(self, k):
        if isinstance(k, self.__class__):
            return self.__class__((operator.getitem, self, k),
                                  "%s[%s]" % (self._format, k._format),
                                  dict(list(self._format_args.items()) + list(k._format_args.items())),
                                  self._arity + k._arity)
        item_name = _random_name()
        return self.__class__(F(operator.itemgetter(k)) << F(self),
                              "%s[%%(%s)r]" % (self._format,item_name),
                              dict(list(self._format_args.items()) + [(item_name,k)]),
                              self._arity)

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

        r = r % self._format_args
        return "({left}) => {right}".format(left=", ".join(l), right=r)

    def __repr__(self):
        """Return original function notation to ensure that eval(repr(f)) == f"""
        return re.sub(r"x\d+", "_", str(self).split("=>", 1)[1].strip())

    def __call__(self, *args):
        if len(args) != self._arity:
            raise ArityError(self, self._arity, len(args))

        if not isinstance(self._callback, tuple):
            return self._callback(*args)

        f, left, right = self._callback
        return f(left(*args[:left._arity]), right(*args[left._arity:]))

    __add__ = fmap(operator.add, "self + other")
    __mul__ = fmap(operator.mul, "self * other")
    __sub__ = fmap(operator.sub, "self - other")
    __mod__ = fmap(operator.mod, "self %% other")
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

    __neg__ = unary_fmap(operator.neg, "-self")
    __pos__ = unary_fmap(operator.pos, "+self")
    __invert__ = unary_fmap(operator.invert, "~self")

    __radd__ = fmap(flip(operator.add), "other + self")
    __rmul__ = fmap(flip(operator.mul), "other * self")
    __rsub__ = fmap(flip(operator.sub), "other - self")
    __rmod__ = fmap(flip(operator.mod), "other %% self")
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
