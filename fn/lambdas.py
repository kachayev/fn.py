from .operator import identity

class _Callable(object):
	def __init__(self, callback=None):
		self.callback = callback or identity

	def __add__(self, other):
		# should be implemented with folding by apply operator
		return _Callable(lambda *args, **kwargs: self.callback(*args, **kwargs) + other)

	def __call__(self, *args, **kwargs):
		return self.callback(*args, **kwargs)

shortcut = _Callable()