Fn.py: enjoy FP in Python
=========================

Despite the fact that Python is not pure-functional programming
language, it's multi-paradigm PL and it gives you enough freedom to take
credits from functional programming approach. There are theoretical and
practical advantages to the functional style:

-  Formal provability
-  Modularity
-  Composability
-  Ease of debugging and testing

``Fn.py`` library provides you with missing "batteries" to get maximum
from functional approach even in mostly-imperative program.

More about functional approach from my Pycon UA 2012 talks: `Functional
Programming with
Python <http://ua.pycon.org/static/talks/kachayev/#/>`_.

Scala-style lambdas definition
------------------------------

.. code-block:: python

    from fn import _
    from fn.op import zipwith
    from itertools import repeat

    assert list(map(_ * 2, range(5))) == [0,2,4,6,8]
    assert list(filter(_ < 10, [9,10,11])) == [9]
    assert list(zipwith(_ + _)([0,1,2], repeat(10))) == [10,11,12]

More examples of using ``_`` you can find in `test
cases <https://github.com/kachayev/fn.py/blob/master/tests.py>`_
declaration (attributes resolving, method calling, slicing).

**Attention!** If you work in interactive python shell, your should remember that ``_`` means "latest output" and you'll get unpredictable results. In this case, you can do something like ``from fn import _ as X`` (and then write functions like ``X * 2``).

If you are not sure, what your function is going to do, you can print it:

.. code-block:: python

    from fn import _

    print (_ + 2) # "(x1) => (x1 + 2)"
    print (_ + _ * _) # "(x1, x2, x3) => (x1 + (x2 * x3))"


Streams and infinite sequences declaration
------------------------------------------

Lazy-evaluated scala-style streams. Basic idea: evaluate each new
element "on demand" and share calculated elements between all created
iterators. ``Stream`` object supports ``<<`` operator that means pushing
new elements when it's necessary.

Simplest cases:

.. code-block:: python

    from fn import Stream

    s = Stream() << [1,2,3,4,5]
    assert list(s) == [1,2,3,4,5]
    assert s[1] == 2
    assert list(s[0:2]) == [1,2]

    s = Stream() << range(6) << [6,7]
    assert list(s) == [0,1,2,3,4,5,6,7]

    def gen():
        yield 1
        yield 2
        yield 3

    s = Stream() << gen << (4,5)
    assert list(s) == [1,2,3,4,5]

Lazy-evaluated stream is useful for infinite sequences, i.e. fibonacci
sequence can be calculated as:

.. code-block:: python

    from fn import Stream
    from fn.iters import take, drop, map
    from operator import add

    f = Stream()
    fib = f << [0, 1] << map(add, f, drop(1, f))

    assert list(take(10, fib)) == [0,1,1,2,3,5,8,13,21,34]
    assert fib[20] == 6765
    assert list(fib[30:35]) == [832040,1346269,2178309,3524578,5702887]

High-level operations with functions
------------------------------------

``fn.F`` is a useful function wrapper to provide easy-to-use partial
application and functions composition.

.. code-block:: python

    from fn import F, _
    from operator import add, mul

    # F(f, *args) means partial application 
    # same as functools.partial but returns fn.F instance
    assert F(add, 1)(10) == 11

    # F << F means functions composition,
    # so (F(f) << g)(x) == f(g(x))
    f = F(add, 1) << F(mul, 100)
    assert list(map(f, [0, 1, 2])) == [1, 101, 201]
    assert list(map(F() << str << (_ ** 2) << (_ + 1), range(3))) == ["1", "4", "9"]

You can find more examples for compositions usage in ``fn._``
implementation `source
code <https://github.com/kachayev/fn.py/blob/master/fn/underscore.py>`__.

``fn.op.apply`` executes given function with given positional arguments
in list (or any other iterable). ``fn.op.flip`` returns you function
that will reverse arguments order before apply.

.. code-block:: python

    from fn.op import apply, flip
    from operator import add, sub

    assert apply(add, [1, 2]) == 3
    assert flip(sub)(20,10) == -10
    assert list(map(apply, [add, mul], [(1,2), (10,20)])) == [3, 200]

Itertools recipes
-----------------

``fn.iters`` module consists from two parts. First one is "unification"
of lazy functionality for few functions to work the same way in Python
2+/3+:

-  ``map`` (returns ``itertools.imap`` in Python 2+)
-  ``filter`` (returns ``itertools.ifilter`` in Python 2+)
-  ``reduce`` (returns ``functools.reduce`` in Python 3+)
-  ``zip`` (returns ``itertools.izip`` in Python 2+)
-  ``range`` (returns ``xrange`` in Python 2+)
-  ``filterfalse`` (returns ``itertools.ifilterfalse`` in Python 2+)
-  ``zip_longest`` (returns ``itertools.izip_longest`` in Python 2+)

Second part of module is high-level recipes to work with iterators. Most
of them taken from `Python
docs <http://docs.python.org/2.7/library/itertools.html#itertools.product>`_
and adopted to work both with Python 2+/3+. Such recipes as ``drop``,
``takelast``, ``droplast``, ``splitat``, ``splitby`` I have already
submitted as `docs patch <http://bugs.python.org/issue16774>`_ which is
review status just now.

-  ``take``, ``drop``
-  ``takelast``, ``droplast``
-  ``head``, ``tail``
-  ``consume``
-  ``nth``
-  ``padnone``, ``ncycles``
-  ``repeatfunc``
-  ``grouper``, ``powerset``, ``pairwise``
-  ``roundrobin``
-  ``partition``, ``splitat``, ``splitby``
-  ``flatten``
-  ``iter_except``

More information about use cases you can find in docstrings for each
function in `source
code <https://github.com/kachayev/fn.py/blob/master/fn/iters.py>`__ and
in `test
cases <https://github.com/kachayev/fn.py/blob/master/tests.py>`_.

Functional style for error-handling
-----------------------------------

-  Maybe
-  Either

**TODO: Implementation, code samples**

Trampolines decorator
---------------------

Workaround for dealing with TCO without heavy stack utilization.

**TODO: Implementation, code samples and documented theory.**

Installation
------------

To install ``fn.py``, simply:

.. code-block:: console

    $ pip install fn

Or, if you absolutely must:

.. code-block:: console

    $ easy_install fn

You can also build library from source

.. code-block:: console

    $ git clone https://github.com/kachayev/fn.py.git
    $ cd fn.py
    $ python setup.py install

Work in progress (!)
--------------------

"Roadmap":

-  Trampolines decorator
-  Error handling (``Maybe``, ``Either`` from Haskell, ``Option`` from
   Scala etc)
-  Add to ``fn.iters`` module ``foldl``, ``foldr``, ``findelem``,
   ``findindex``
-  C-accelerator for most modules

Ideas to think about:

-  "Pipeline" notation for composition (back-order):
   ``F() >> list >> partial(map, int)``
-  Curried function builder to simplify
   ``lambda arg1: lambda arg2: ...``
-  Scala-style for-yield loop to simplify long map/filter blocks

Contribute
----------

1. Check for open issues or open a fresh issue to start a discussion
   around a feature idea or a bug.
2. Fork the repository on Github to start making your changes to the
   master branch (or branch off of it).
3. Write a test which shows that the bug was fixed or that the feature
   works as expected.
