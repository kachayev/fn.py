"""
``fn.monad.Option`` represents optional values, each instance of 
``Option`` can be either instance of ``Full`` or ``Empty``. 
It provides you with simple way to write long computation sequences 
and get rid of many ``if/else`` blocks. See usage examples below. 

Assume that you have ``Request`` class that gives you parameter 
value by its name. To get uppercase notation for non-empty striped value:

    class Request(dict):
        def parameter(self, name):
            return self.get(name, None)

    r = Request(testing="Fixed", empty="   ")
    param = r.parameter("testing")
    if param is None:
        fixed = ""
    else:
        param = param.strip()
        if len(param) == 0:
            fixed = ""
        else:
            fixed = param.upper()


Hmm, looks ugly.. Update code with ``fn.monad.Option``:

    from operator import methodcaller
    from fn.monad import optionable

    class Request(dict):
        @optionable
        def parameter(self, name):
            return self.get(name, None)

    r = Request(testing="Fixed", empty="   ")
    fixed = r.parameter("testing")
             .map(methodcaller("strip"))
             .filter(len)
             .map(methodcaller("upper"))
             .getOr("")

``fn.monad.Option.orCall`` is good method for trying several 
variant to end computation. I.e. use have ``Request`` class 
with optional attributes ``type``, ``mimetype``, ``url``. 
You need to evaluate "request type" using at least on attribute:

    from fn.monad import Option

    request = dict(url="face.png", mimetype="PNG")
    tp = Option(request.get("type", None)) \ # check "type" key first
            .orCall(from_mimetype, request) \ # or.. check "mimetype" key
            .orCall(from_extension, request) \ # or... get "url" and check extension
            .getOr("application/undefined")


"""

from collections import namedtuple
from functools import wraps, partial
from operator import eq, is_not

class Option(object):

    def __new__(tp, value, checker=partial(is_not, None)):
        if isinstance(value, Option):
            # Option(Full) -> Full
            # Option(Empty) -> Empty
            return value

        return Full(value) if checker(value) else Empty()

    @staticmethod
    def from_value(value):
        return Option(value)

    @staticmethod
    def from_call(callback, *args, **kwargs):
        """Execute callback and catch possible (all by default)
        exceptions. If exception is raised Empty will be returned.
        """
        exc = kwargs.pop("exc", Exception)
        try:
            return Option(callback(*args, **kwargs)) 
        except exc:
            return Empty()

class Full(Option):
    """Represents value that is ready for further computations"""

    __slots__ = "x", 

    def __new__(tp, *args, **kwargs):
        return object.__new__(tp)

    def __init__(self, value, *args):
        # Option(Full) -> Full
        self.x = value.getOr("") if isinstance(value, Full) else value

    def map(self, callback):
        return Full(callback(self.x))

    def filter(self, callback):
        return self if callback(self.x) else Empty()

    def exists(self, callback):
        # XXX: need to reimplement this method and 
        # add isEmpty (or something like this) instead
        return True 

    def getOr(self, default):
        return self.x

    def getOrCall(self, callback, *args, **kwargs):
        return self.x

    def orElse(self, default):
        return self

    def orCall(self, callback, *args, **kwargs):
        return self

    def __str__(self):
        return "Full(%s)" % self.x

    __repr__ = __str__

    def __eq__(self, other):
        if not isinstance(other, Full):
            return False
        return eq(self.x, other.x)


class Empty(Option):
    """Represents empty option (without value)"""

    __object = None

    def __new__(tp, *args, **kwargs):
        if Empty.__object is None:
            Empty.__object = object.__new__(tp)
        return Empty.__object

    def map(self, callback):
        return Empty()

    def filter(self, callback):
        return Empty()

    def exists(self, callback):
        return False

    def getOr(self, default):
        return default

    def getOrCall(self, callback, *args, **kwargs):
        return callback(*args, **kwargs)

    def orElse(self, default):
        return Option(default)

    def orCall(self, callback, *args, **kwargs):
        return Option(callback(*args, **kwargs))

    def __str__(self):
        return "Empty()"

    __repr__ = __str__

    def __eq__(self, other):
        return isinstance(other, Empty)

def optionable(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return Option(f(*args, **kwargs))
    
    return wrapper