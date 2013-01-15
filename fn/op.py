identity = lambda arg: arg

def curry(f, arg, *rest):
	return curry(f(arg), *rest) if rest else f(arg)