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
Python <http://kachayev.github.com/talks/uapycon2012/index.html>`_.

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

``_`` will fail with ``ArityError`` (``TypeError`` subclass) on inaccurate number of passed arguments. This is one more restrictions to ensure that you did everything right:

.. code-block:: python

    >>> from fn import _
    >>> (_ + _)(1)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "fn/underscore.py", line 82, in __call__
        raise ArityError(self, self._arity, len(args))
    fn.underscore.ArityError: (_ + _) expected 2 arguments, got 1


Persistent data structures
--------------------------

**Attention:** Persistent data structures are under active development.

Persistent data structure is a data structure that always preserves the previous version of itself when it is modified (more formal information on `Wikipedia <http://goo.gl/8VveOH>`_). Each operation with such data structure yields a new updated structure instead of in-place modification (all previous versions are potentially available or GC-ed when possible).

Lets take a quick look:

.. code-block:: python

    >>> from fn.immutable import SkewHeap
    >>> s1 = SkewHeap(10)
    >>> s2 = s1.insert(20)
    >>> s2
    <fn.immutable.heap.SkewHeap object at 0x10b14c050>
    >>> s3 = s2.insert(30)
    >>> s3
    <fn.immutable.heap.SkewHeap object at 0x10b14c158> # <-- other object
    >>> s3.extract()
    (10, <fn.immutable.heap.SkewHeap object at 0x10b14c050>)
    >>> s3.extract() # <-- s3 isn't changed
    (10, <fn.immutable.heap.SkewHeap object at 0x10b11c052>)

If you think I'm totally crazy and it will work despairingly slow, just give it 5 minutes. Relax, take a deep breath and read about few techniques that make persistent data structures fast and efficient: `structural sharing <http://en.wikipedia.org/wiki/Persistent_data_structure#Examples_of_persistent_data_structures>`_ and `path copying <http://en.wikipedia.org/wiki/Persistent_data_structure#Path_Copying>`_.

To see how it works in "pictures", you can check great slides from Zach Allaun's talk (StrangeLoop 2013): `"Functional Vectors, Maps And Sets In Julia" <http://goo.gl/Cp1Qsq>`_.

And, if you are brave enough, go and read:

- Chris Okasaki, "Purely Functional Data Structures" (`Amazon <http://goo.gl/c7ptkk>`_)
- Fethi Rabhi and Guy Lapalme, "Algorithms: A Functional Programming Approach" (`Amazon <http://goo.gl/00BxTO>`_)

Available immutable data structures in ``fn.immutable`` module:

- ``LinkedList``: most "obvious" persistent data structure, used as building block for other list-based structures (stack, queue)
- ``Stack``: wraps linked list implementation with well-known pop/push API
- ``Queue``: uses two linked lists and lazy copy to provide O(1) enqueue and dequeue operations
- ``Deque`` (in progress): `"Confluently Persistent Deques via Data
  Structural Bootstrapping" <http://goo.gl/vVTzx3>`_
- ``Deque`` based on ``FingerTree`` data structure (see more information below)
- ``Vector``: O(log32(n)) access to elements by index (which is near-O(1) for reasonable vector size), implementation is based on ``BitmappedTrie``, almost drop-in replacement for built-in Python ``list``
- ``SkewHeap``: self-adjusting heap implemented as a binary tree with specific branching model, uses heap merge as basic operation, more information - `"Self-adjusting heaps" <http://goo.gl/R1PZME>`_
- ``PairingHeap``: `"The Pairing-Heap: A New Form of Self-Adjusting Heap" <http://goo.gl/aiVtPH>`_
- ``Dict`` (in progress): persistent hash map implementation based on ``BitmappedTrie``
- ``FingerTree`` (in progress): `"Finger Trees: A Simple General-purpose Data Structure" <http://goo.gl/Bzo0df>`_

Use appropriate doc strings to get more information about each data structure as well as sample code.

To get more clear vision of how persistent heaps work (``SkewHeap`` and ``PairingHeap``), you can look at slides from my talk `"Union-based heaps" <http://goo.gl/VMgdG2>`_ (with analyzed data structures definitions in Python and Haskell).

**Note.** Most functional languages use persistent data structures as basic building blocks, well-known examples are Clojure, Haskell and Scala. Clojure community puts much effort to popularize programming based on the idea of data immutability. There are few amazing talk given by Rich Hickey (creator of Clojure), you can check them to find answers on both questions "How?" and "Why?":

- `"The Value of Values" <http://goo.gl/137UG5>`_
- `"Persistent Data Structures and Managed References" <http://goo.gl/M3vZ7E>`_

Streams and infinite sequences declaration
------------------------------------------

Lazy-evaluated Scala-style streams. Basic idea: evaluate each new
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

Trampolines decorator
---------------------

``fn.recur.tco`` is a workaround for dealing with TCO without heavy stack utilization. Let's start from simple example of recursive factorial calculation:

.. code-block:: python

    def fact(n):
        if n == 0: return 1
        return n * fact(n-1)

This variant works, but it's really ugly. Why? It will utilize memory too heavy cause of recursive storing all previous values to calculate final result. If you will execute this function with big ``n`` (more than ``sys.getrecursionlimit()``) CPython will fail with

.. code-block:: python

    >>> import sys
    >>> fact(sys.getrecursionlimit() * 2)
    ... many many lines of stacktrace ...
    RuntimeError: maximum recursion depth exceeded

Which is good, cause it prevents you from terrible mistakes in your code.

How can we optimize this solution? Answer is simple, lets transform function to use tail call:

.. code-block:: python

    def fact(n, acc=1):
        if n == 0: return acc
        return fact(n-1, acc*n)

Why this variant is better? Cause you don't need to remember previous values to calculate final result. More about `tail call optimization <http://en.wikipedia.org/wiki/Tail_call>`_ on Wikipedia. But... Python interpreter will execute this function the same way as previous one, so you won't win anything.

``fn.recur.tco`` gives you mechanism to write "optimized a bit" tail call recursion (using "trampoline" approach):

.. code-block:: python

    from fn import recur

    @recur.tco
    def fact(n, acc=1):
        if n == 0: return False, acc
        return True, (n-1, acc*n)

``@recur.tco`` is a decorator that execute your function in ``while`` loop and check output:

- ``(False, result)`` means that we finished
- ``(True, args, kwargs)`` means that we need to call function again with other arguments
- ``(func, args, kwargs)`` to switch function to be executed inside while loop

The last variant is really useful, when you need to switch callable inside evaluation loop. Good example for such situation is recursive detection if given number is odd or even:

.. code-block:: python

    >>> from fn import recur
    >>> @recur.tco
    ... def even(x):
    ...     if x == 0: return False, True
    ...     return odd, (x-1,)
    ...
    >>> @recur.tco
    ... def odd(x):
    ...     if x == 0: return False, False
    ...     return even, (x-1,)
    ...
    >>> print even(100000)
    True

**Attention:** be careful with mutable/immutable data structures processing.

Itertools recipes
-----------------

``fn.uniform`` provides you with "unification"
of lazy functionality for few functions to work the same way in Python
2+/3+:

-  ``map`` (returns ``itertools.imap`` in Python 2+)
-  ``filter`` (returns ``itertools.ifilter`` in Python 2+)
-  ``reduce`` (returns ``functools.reduce`` in Python 3+)
-  ``zip`` (returns ``itertools.izip`` in Python 2+)
-  ``range`` (returns ``xrange`` in Python 2+)
-  ``filterfalse`` (returns ``itertools.ifilterfalse`` in Python 2+)
-  ``zip_longest`` (returns ``itertools.izip_longest`` in Python 2+)
-  ``accumulate`` (backported to Python < 3.3)

``fn.iters`` is high-level recipes to work with iterators. Most
of them taken from `Python
docs <http://docs.python.org/2.7/library/itertools.html#itertools.product>`_
and adopted to work both with Python 2+/3+. Such recipes as ``drop``,
``takelast``, ``droplast``, ``splitat``, ``splitby`` I have already
submitted as `docs patch <http://bugs.python.org/issue16774>`_ which is
review status just now.

-  ``take``, ``drop``
-  ``takelast``, ``droplast``
-  ``head`` (alias: ``first``), ``tail`` (alias: ``rest``)
-  ``second``, ``ffirst``
-  ``compact``, ``reject``
-  ``every``, ``some``
-  ``iterate``
-  ``consume``
-  ``nth``
-  ``padnone``, ``ncycles``
-  ``repeatfunc``
-  ``grouper``, ``powerset``, ``pairwise``
-  ``roundrobin``
-  ``partition``, ``splitat``, ``splitby``
-  ``flatten``
-  ``iter_except``
-  ``first_true``

More information about use cases you can find in docstrings for each
function in `source
code <https://github.com/kachayev/fn.py/blob/master/fn/iters.py>`__ and
in `test
cases <https://github.com/kachayev/fn.py/blob/master/tests.py>`_.

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

It also give you move readable in many cases "pipe" notation to deal with functions composition:

.. code-block:: python

    from fn import F, _
    from fn.iters import filter, range

    func = F() >> (filter, _ < 6) >> sum
    assert func(range(10)) == 15

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

``fn.op.foldl`` and ``fn.op.foldr`` are folding operators. Each accepts function with arity 2 and returns function that can be used to reduce iterable to scalar: from left-to-right and from right-to-left in case of ``foldl`` and ``foldr`` respectively.

.. code-block:: python

    from fn import op, _

    folder = op.foldr(_ * _, 1)
    assert 6 == op.foldl(_ + _)([1,2,3])
    assert 6 == folder([1,2,3])

Use case specific for right-side folding is:

.. code-block:: python

    from fn.op import foldr, call

    assert 100 == foldr(call, 0 )([lambda s: s**2, lambda k: k+10])
    assert 400 == foldr(call, 10)([lambda s: s**2, lambda k: k+10])


Function currying
-----------------

``fn.func.curried`` is a decorator for building curried functions, for example:

.. code-block:: python

    >>> from fn.func import curried
    >>> @curried
    ... def sum5(a, b, c, d, e):
    ...     return a + b + c + d + e
    ...
    >>> sum5(1)(2)(3)(4)(5)
    15
    >>> sum5(1, 2, 3)(4, 5)
    15


Functional style for error-handling
-----------------------------------

``fn.monad.Option`` represents optional values, each instance of ``Option`` can be either instance of ``Full`` or ``Empty``. It provides you with simple way to write long computation sequences and get rid of many ``if/else`` blocks. See usage examples below.

Assume that you have ``Request`` class that gives you parameter value by its name. To get uppercase notation for non-empty striped value:

.. code-block:: python

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

.. code-block:: python

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
             .get_or("")

``fn.monad.Option.or_call`` is good method for trying several variant to end computation. I.e. use have ``Request`` class with optional attributes ``type``, ``mimetype``, ``url``. You need to evaluate "request type" using at least one attribute:

.. code-block:: python

    from fn.monad import Option

    request = dict(url="face.png", mimetype="PNG")
    tp = Option \
            .from_value(request.get("type", None)) \ # check "type" key first
            .or_call(from_mimetype, request) \ # or.. check "mimetype" key
            .or_call(from_extension, request) \ # or... get "url" and check extension
            .get_or("application/undefined")


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

Work in progress
----------------

"Roadmap":

- ``fn.monad.Either`` to deal with error logging
-  C-accelerator for most modules

Ideas to think about:

-  Scala-style for-yield loop to simplify long map/filter blocks

Contribute
----------

1. Check for open issues or open a fresh issue to start a discussion
   around a feature idea or a bug.
2. Fork the repository on Github to start making your changes to the
   master branch (or branch off of it).
3. Write a test which shows that the bug was fixed or that the feature
   works as expected.

How to find me
--------------

- Twitter: `@kachayev <https://twitter.com/kachayev>`_
- Email: kachayev <at> gmail.com
