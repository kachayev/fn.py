from collections import namedtuple

"""Provides decorator to deal with tail calls in recursive function."""

class tco(object):
    """Provides a trampoline for functions that need one.

    Such function should return one of:
     * (False, result) - will exit from loop and return result to caller
     * (True, args) or (True, args, kwargs) - will repeat loop with the same
                                              function and other arguments
     * (func, args) or (func, kwargs) - will repeat loop with new callable
                                        and new arguments 

    Usage example:

    @recur.tco
    def accumulate(origin, f=operator.add, acc=0):
        n = next(origin, None)
        if n is None: return False, acc
        return True, (origin, f, f(acc, n))

    Idea was described on python mailing list:
    http://mail.python.org/pipermail/python-ideas/2009-May/004486.html    
    """

    __slots__ = "func", 

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        action = self
        while True:
            result = action.func(*args, **kwargs)
            # return final result
            if not result[0]: return result[1]

            # next loop with other arguments
            act, args = result[:2]
            # it's possible to given other function to run
            # XXX: do I need to raise exception if it's 
            # impossible to use such function in tail calls loop?
            if callable(act): action = act
            kwargs = result[2] if len(result) > 2 else {}

class stackless(object):
    """Provides a "stackless" (constant Python stack) recursion decorator
    for generators.

    Invoking as f() creates the control structures. Within a
    function, only use `yield f.call()` and `yield f.tailcall()`.

    Usage examples:

    Tail call optimised recursion with tailcall():

    @recur.stackless
    def fact(n, acc=1):
        if n == 0:
            yield acc
            return
        yield fact.tailcall(n-1, n*acc)

    Non-tail recursion with call() uses heap space so won't overflow:

    @recur.stackless
    def fib(n):
        if n == 0:
            yield 1
            return
        if n == 1:
            yield 1
            return
        yield (yield fib.call(n-1)) + (yield fib.call(n-2))

    Mutual recursion also works:

    @recur.stackless
    def is_odd(n):
        if n == 0:
            yield False
            return
        yield is_even.tailcall(n-1)

    @recur.stackless
    def is_even(n):
        if n == 0:
            yield True
            return
        yield is_odd.tailcall(n-1)
    """

    __slots__ = "func",

    Thunk = namedtuple('Thunk', ("func", "args", "kwargs", "is_tailcall"))

    def __init__(self, func):
        self.func = func

    def call(self, *args, **kwargs):
        return self.Thunk(self.func, args, kwargs, False)

    def tailcall(self, *args, **kwargs):
        return self.Thunk(self.func, args, kwargs, True)

    def __call__(self, *args, **kwargs):
        s = [self.func(*args, **kwargs)]
        r = []
        while s:
            try:
                if r:
                    v = s[-1].send(r[-1])
                    r.pop()
                else:
                    v = next(s[-1])
            except StopIteration:
                s.pop()
                continue

            if isinstance(v, self.Thunk):
                g = v.func(*v.args, **v.kwargs)
                if v.is_tailcall:
                    s[-1] = g
                else:
                    s.append(g)
            else:
                r.append(v)
        return r[0]
