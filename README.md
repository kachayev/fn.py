# Fn.py: enjoy FP in Python

General description

## Streams

Lazy-evaluated scala-style streams. Basic idea: evaluate each new element "on demand" and share calculated elements between all created iterators. `Stream` object supports `<<` operator that means pushing new elements when it's necessary.

Simplest cases:

    from fn import Stream
    
    s = Stream() << [1,2,3,4,5]
    assert list(s) == [1,2,3,4,5]
    assert s[1] == 2
    assert s[0:2] == [1,2]

    s = Stream() << range(6) << [6,7]
    assert list(s) == [0,1,2,3,4,5,6,7]

    def gen():
        yield 1
        yield 2
        yield 3
    
    s = Stream() << gen << (4,5)
    assert list(s) == [1,2,3,4,5]

Lazy-evaluated stream is useful for infinite sequences, i.e. fibonacci sequence can be calculated as:

    from fn import Stream
    from fn.iters import take, drop, map

    f = Stream()
    fib = f << [0, 1] << map(add, f, drop(1, f))

    assert list(take(10, fib)) == [0,1,1,2,3,5,8,13,21,34]
    assert fib[20] == 6765
    assert fib[30:35] == [832040,1346269,2178309,3524578,5702887]

## Scala-style lambdas definition


    from fn import _
    from fn.iters import zipwith
    from itertools import repeat

    assert list(map(_ * 2, range(5))) == [0,2,4,6,8]
    assert list(filter(_ < 10, [9,10,11])) == [9]
    assert list(zipwith(_ + _, [0,1,2], repeat(10))) == [10,11,12]


## High-level operations with functions

    from fn import F, _
    from fn.operator import apply, flip
    from operator import add, mul

    # F(add, 1) == F.partial(add, 1)
    mul_100_add_1 = F(add, 1) << F(mul, 100)
    # F << F means functions composition, so
    # (F(f) << F(g))(x) == f(g(x))
    assert list(map(mul_100_add_1, [0,1,2])) == [1,101,201]

    # Simplify syntax for composition:
    # F << f1 << f2 << f3 << ..
    assert list(map(F << (_ ** 2) << _ + 1, range(3))) == [2, 4, 6]

	# Apply and flip operator useful for map, filter, fold operations    
	assert apply(add, [1, 2]) == 3
	assert flip([10, 20], mul) == 200
	assert list(map(apply, [add, mul], [(1,2), (10,20)])) == [3, 200]

__TODO: more interesting examples for functional composition__

## Itertools receipts

* take, drop, takelast, droplast
* first, rest
* partition
* splitat, splitby
* flatten
* foldl, foldr, zipwith
* findelem, findindex

## Functional style for error-handling

* Maybe
* Either

__TODO: Implementation, code samples__

## Trampolines decorator

Workaround for dealing with TCO without heavy stack utilization.

__TODO: Implementation, code samples and documented theory.__

## Installation

To install `fn.py`, simply:

    $ pip install fn

Or, if you absolutely must:

    $ easy_install fn

You can also build library from source

    $ git clone https://github.com/kachayev/fn.py.git
    $ cd fn.py
    $ python setup.py install

## Plan

* Scala-style lambda implementation
* Unit tests for `Stream` and `underscore` module, tests infrastructure
* Itertools, operators
* Functions composition and good example for its usage
* Error handling (`Maybe`, `Either` from Haskell, `Option` from Scala etc)
* Trampolines decorator
* C-accelerator for most modules

## Contribute

1. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
2. Fork the repository on Github to start making your changes to the master branch (or branch off of it).
3. Write a test which shows that the bug was fixed or that the feature works as expected.
