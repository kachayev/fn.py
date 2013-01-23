import sys
import operator

from .op import apply, curry, flip, identity
from .func import F


_div = operator.div if sys.hexversion < 0x03000000 else operator.truediv


def f(text, g):
    def op(a, b=None):
        new_repr = text.format(a, b)

        return (
            # FIXME ideally, it should use partially-applied format strings
            #   instead of those placeholders.
            #   The original underscore.py suffered from the same bug,
            #   though, so I decided to upload the code anyway.
            T(lambda x: f('<lambda>', g)(a(x), b), new_repr) if isinstance(a, T) else
            T(lambda x: f('<lambda>', g)(a, b(x)), new_repr) if isinstance(b, T) else
            g(a) if b is None else g(a, b)
        )

    return op


class T(object):

    __slots__ = ('_callback', '_format')

    def __init__(self, callback=identity, format='_'):
        super(object, self).__init__()
        self._callback = callback
        self._format = format

    def __call__(self, *args):
        return curry(self._callback, *args)

    def __repr__(self):
        return self._format

    def call(self, name):
        return T(F(apply) << operator.attrgetter(name) << F(self))

    __getattr__  = f('getattr({!r}, {!r})', getattr)
    __getitem__  = f('{!r}[{!r}]',          operator.getitem)
    __contains__ = f('{1!r} in {0!r}',      operator.contains)

    __add__ = f('({!r} + {!r})',  operator.add)
    __mul__ = f('({!r} * {!r})',  operator.mul)
    __sub__ = f('({!r} - {!r})',  operator.sub)
    __mod__ = f('({!r} % {!r})',  operator.mod)
    __pow__ = f('({!r} ** {!r})', operator.pow)

    __and__ = f('({!r} & {!r})', operator.and_)
    __or__  = f('({!r} | {!r})', operator.or_)
    __xor__ = f('({!r} ^ {!r})', operator.xor)

    __div__      = f('({!r} / {!r})',      _div)
    __truediv__  = f('({!r} / {!r})',      _div)
    __floordiv__ = f('({!r} // {!r})',     operator.floordiv)
    __divmod__   = f('divmod({!r}, {!r})', divmod)

    __lshift__ = f('({!r} << {!r})', operator.lshift)
    __rshift__ = f('({!r} >> {!r})', operator.rshift)

    __lt__ = f('({!r} < {!r})',  operator.lt)
    __le__ = f('({!r} <= {!r})', operator.le)
    __gt__ = f('({!r} > {!r})',  operator.gt)
    __ge__ = f('({!r} >= {!r})', operator.ge)
    __eq__ = f('({!r} == {!r})', operator.eq)
    __ne__ = f('({!r} != {!r})', operator.ne)

    __neg__    = f('(-{!r})', operator.neg)
    __pos__    = f('(+{!r})', operator.pos)
    __invert__ = f('(~{!r})', operator.invert)

    __radd__ = f('({1!r} + {0!r})',  flip(operator.add))
    __rmul__ = f('({1!r} * {0!r})',  flip(operator.mul))
    __rsub__ = f('({1!r} - {0!r})',  flip(operator.sub))
    __rmod__ = f('({1!r} % {0!r})',  flip(operator.mod))
    __rpow__ = f('({1!r} ** {0!r})', flip(operator.pow))

    __rand__ = f('({1!r} & {0!r})', flip(operator.and_))
    __ror__  = f('({1!r} | {0!r})', flip(operator.or_))
    __rxor__ = f('({1!r} ^ {0!r})', flip(operator.xor))

    __rdiv__      = f('({1!r} / {0!r})',      flip(_div))
    __rtruediv__  = f('({1!r} / {0!r})',      flip(_div))
    __rfloordiv__ = f('({1!r} // {0!r})',     flip(operator.floordiv))
    __rdivmod__   = f('divmod({1!r}, {0!r})', flip(divmod))

    __rlshift__ = f('({1!r} << {0!r})', flip(operator.lshift))
    __rrshift__ = f('({1!r} >> {0!r})', flip(operator.rshift))


shortcut = T()
