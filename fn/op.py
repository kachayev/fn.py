from sys import version

identity = lambda arg: arg
apply = apply if version.startswith("2") else _apply

def _apply(f, args, kwargs=None):
    return f(*args, **(kwargs or {}))

def curry(f, arg, *rest):
    return curry(f(arg), *rest) if rest else f(arg)

