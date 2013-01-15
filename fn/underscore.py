import operator
from .op import identity, curry

def fmap(f):
	def applyier(self, other):
		if isinstance(other, self.__class__):
			# XXX this should be fmap
			return self.__class__(lambda arg1: lambda arg2: f(self(arg1), other(arg2)))
		# XXX this should be composition
		return self.__class__(lambda arg: f(self(arg), other))
	return applyier

# XXX Deal with code duplication with composition and fabric method
class _Callable(object):

	def __init__(self, callback=None):
		self._callback = callback or identity

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

	__contains__ = fmap(operator.contains)
	
	def __nonzero__(self):
		# XXX this should be composition
		return self.__class__(lambda arg: bool(self(arg)))

	def __getattr__(self, name):
		return self.__class__(lambda arg: getattr(self(arg), name))

	def call(self, name, *args):
		"""Call method from _ object by given name and arguments"""
		return self.__class__(lambda arg: getattr(self(arg), name)(*args))

	def __getitem__(self, k):
		if isinstance(k, self.__class__):
			# XXX this should be fmap
			return self.__class__(lambda arg1: lambda arg2: self(arg1)[k(arg2)])
		# XXX this should be composition
		return self.__class__(lambda arg: self(arg)[k])

	def __str__(self):
		"""Build readable representation for function

		(_ < 7): (x1) => (x1 < 7)
		(_ + _*10): (x1, x2) => (x1 + x2*10)
		"""
		raise NotImplementedError

	def __call__(self, *args):
		return curry(self._callback, *args)

	def __neg__(self):
		raise NotImplementedError
	def __pos__(self):
		raise NotImplementedError
	def __invert__(self):
		raise NotImplementedError

	def __radd__(self, other):
		raise NotImplementedError
	def __rsub__(self, other):
		raise NotImplementedError
	def __rmul__(self, other):
		raise NotImplementedError
	def __rdiv__(self, other):
		raise NotImplementedError
	def __rtruediv__(self, other):
		raise NotImplementedError
	def __rfloordiv__(self, other):
		raise NotImplementedError
	def __rmod__(self, other):
		raise NotImplementedError
	def __rdivmod__(self, other):
		raise NotImplementedError
	def __rpow__(self, other):
		raise NotImplementedError
	def __rlshift__(self, other):
		raise NotImplementedError
	def __rrshift__(self, other):
		raise NotImplementedError
	def __rand__(self, other):
		raise NotImplementedError
	def __rxor__(self, other):
		raise NotImplementedError
	def __ror__(self, other):
		raise NotImplementedError

shortcut = _Callable()