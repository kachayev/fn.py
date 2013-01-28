"""
Example of Option usage (from Scala documentation):

    val name: Option[String] = request getParameter "name"
    val upper = name map { _.trim } filter { _.length != 0 } map { _.toUpperCase }
    println(upper getOrElse "")

Python variant:

    name = request.parameter("name")
    print name.map(methodcaller(trim))
              .filter(len)
              .map(methodcaller("upper"))
              .getOr("")
"""

from collections import namedtuple
from functools import wraps

class Option(object):

    def __new__(tp, value, checker=bool):
        if isinstance(value, Option):
            # Option(Full) -> Full
            # Option(Empty) -> Empty
            return value

        return Full(value) if checker(value) else Empty()

class Full(Option):

    __slots__ = "x", 
    __new__ = object.__new__

    def __init__(self, value, checker=bool):
        if isinstance(value, Full):
            # Option(Full) -> Full
            self.x = value.getOr("")
        else:
            self.x = value

    def map(self, callback):
        return Full(callback(self.x))

    def filter(self, callback):
        return self if callback(self.x) else Empty()

    def exists(self, callback):
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

class Empty(Option):

    __new__ = object.__new__

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
        return Option(defalut)

    def orCall(self, callback, *args, **kwargs):
        return Option(callback(*args, **kwargs))

    def __str__(self):
        return "Empty()"

    __repr__ = __str__

def optionable(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return Option(f(*args, **kwargs))
    
    return wrapper