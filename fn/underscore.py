from .operator import identity, curry

# XXX Deal with code duplication with composition and fabric method
class _Callable(object):

	def __init__(self, callback=None):
		self._callback = callback or identity

	def __add__(self, other):
		if isinstance(other, self.__class__):
			# XXX this should be fmap
			return self.__class__(lambda arg1: lambda arg2: self(arg1) + other(arg2))
		# XXX this should be composition
		return self.__class__(lambda arg: self(arg) + other)

	def __mul__(self, other):
		if isinstance(other, self.__class__):
			# XXX this should be fmap
			return self.__class__(lambda arg1: lambda arg2: self(arg1) * other(arg2))
		# XXX this should be composition
		return self.__class__(lambda arg: self(arg) * other)

	def __lt__(self, other):
		if isinstance(other, self.__class__):
			# XXX this should be fmap
			return self.__class__(lambda arg1: lambda arg2: self(arg1) < other(arg2))
		# XXX this should be composition
		return self.__class__(lambda arg: self(arg) < other)

	def __le__(self, other):
		if isinstance(other, self.__class__):
			# XXX this should be fmap
			return self.__class__(lambda arg1: lambda arg2: self(arg1) <= other(arg2))
		# XXX this should be composition
		return self.__class__(lambda arg: self(arg) <= other)

	def __gt__(self, other):
		if isinstance(other, self.__class__):
			# XXX this should be fmap
			return self.__class__(lambda arg1: lambda arg2: self(arg1) > other(arg2))
		# XXX this should be composition
		return self.__class__(lambda arg: self(arg) > other)

	def __ge__(self, other):
		if isinstance(other, self.__class__):
			# XXX this should be fmap
			return self.__class__(lambda arg1: lambda arg2: self(arg1) >= other(arg2))
		# XXX this should be composition
		return self.__class__(lambda arg: self(arg) >= other)
	
	def __eq__(self, other):
		if isinstance(other, self.__class__):
			# XXX this should be fmap
			return self.__class__(lambda arg1: lambda arg2: self(arg1) == other(arg2))
		# XXX this should be composition
		return self.__class__(lambda arg: self(arg) == other)

	def __ne__(self, other):
		if isinstance(other, self.__class__):
			# XXX this should be fmap
			return self.__class__(lambda arg1: lambda arg2: self(arg1) != other(arg2))
		# XXX this should be composition
		return self.__class__(lambda arg: self(arg) != other)

	def __nonzero__(self):
		raise NotImplementedError

	def __getattr__(self, name):
		return self.__class__(lambda arg: getattr(self(arg), name))
	def call(self, name, *args):
		"""Call method from _ object by given name and arguments"""
		return self.__class__(lambda arg: getattr(self(arg), name)(*args))

	def __getitem__(self, k):
		raise NotImplementedError
	def __contains__(self, elt):
		raise NotImplementedError

	def __str__(self):
		raise NotImplementedError

	def __call__(self, *args):
		return curry(self._callback, *args)

shortcut = _Callable()