from functools import partial

from .op import identity

class F(object):

	def __init__(self, f = None):
		self.f = f or identity

	@classmethod
	def partial(cls, f, *args, **kwargs):
		return cls(partial(f, *args, **kwargs))

	def __lshift__(self, g):
		return self.__class__(lambda *args, **kwargs: self.f(g(*args, **kwargs)))

	def  __call__(self, *args, **kwargs):
		return self.f(*args, **kwargs)