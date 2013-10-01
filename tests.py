#!/usr/bin/env python

"""Tests for Fn.py library"""

import sys
import unittest
import operator
import itertools

from fn import op, _, F, Stream, iters, underscore, monad, recur

class InstanceChecker(object):
    if sys.version_info[0] == 2 and sys.version_info[1] <= 6:
        def assertIsInstance(self, inst, cls):
            self.assertTrue(isinstance(inst, cls))

class OperatorTestCase(unittest.TestCase):

    def test_currying(self):
        def add(first):
            def add(second):
                return first + second
            return add

        self.assertEqual(1, op.curry(add, 0, 1))

    def test_apply(self):
        self.assertEqual(10, op.apply(operator.add, [2,8]))

    def test_flip(self):
        self.assertEqual(10, op.flip(operator.sub)(2, 12))
        self.assertEqual(-10, op.flip(op.flip(operator.sub))(2, 12))
        # flipping of flipped function should use optimization
        self.assertTrue(operator.sub is op.flip(op.flip(operator.sub)))

    def test_flip_with_shortcut(self):
        self.assertEqual(10, op.flip(_ - _)(2, 12))

    def test_zipwith(self):
        zipper = op.zipwith(operator.add)
        self.assertEqual([10,11,12], list(zipper([0,1,2], itertools.repeat(10))))

        zipper = op.zipwith(_ + _)
        self.assertEqual([10,11,12], list(zipper([0,1,2], itertools.repeat(10))))

        zipper = F() << list << op.zipwith(_ + _)
        self.assertEqual([10,11,12], zipper([0,1,2], itertools.repeat(10)))

    def test_foldl(self):
        self.assertEqual(10, op.foldl(operator.add)([0,1,2,3,4]))
        self.assertEqual(20, op.foldl(operator.add, 10)([0,1,2,3,4]))
        self.assertEqual(20, op.foldl(operator.add, 10)(iters.range(5)))
        self.assertEqual(10, op.foldl(_ + _)(range(5)))

    def test_foldr(self):
        summer = op.foldr(operator.add)
        self.assertEqual(10, op.foldr(operator.add)([0,1,2,3,4]))
        self.assertEqual(20, op.foldr(operator.add, 10)([0,1,2,3,4]))
        self.assertEqual(20, op.foldr(operator.add, 10)(iters.range(5)))
        # specific case for right-side folding
        self.assertEqual(100, 
                         op.foldr(op.call, 0)([lambda s: s**2, lambda k: k+10]))

    def test_unfold_infinite(self):
        doubler = op.unfold(lambda x: (x*2, x*2))
        self.assertEqual(20, next(doubler(10)))
        self.assertEqual([20, 40, 80, 160, 320], list(iters.take(5, doubler(10))))

    def test_unfold_finite(self):
        countdown = op.unfold(lambda x: (x-1, x-2) if x > 1 else None)
        self.assertEqual([9,7,5,3,1], list(countdown(10)))

class UnderscoreTestCase(unittest.TestCase):

    def test_identity_default(self):
        self.assertEqual(10, _(10))

    def test_arithmetic(self):
        # operator +
        self.assertEqual(7, (_ + 2)(5))
        self.assertEqual([10,11,12], list(map(_ + 10, [0,1,2])))
        # operator -
        self.assertEqual(3, (_ - 2)(5))
        self.assertEqual(13, (_ - 2 + 10)(5))
        self.assertEqual([0,1,2], list(map(_ - 10, [10,11,12])))
        # operator * 
        self.assertEqual(10, (_ * 2)(5))
        self.assertEqual(50, (_ * 2 + 40)(5))
        self.assertEqual([0,10,20], list(map(_ * 10, [0,1,2])))
        # operator /
        self.assertEqual(5, (_ / 2)(10))
        self.assertEqual(6, (_ / 2 + 1)(10))
        self.assertEqual([1,2,3], list(map(_ / 10, [10,20,30])))
        # operator **
        self.assertEqual(100, (_ ** 2)(10))
        # operator %
        self.assertEqual(1, (_ % 2)(11))
        # operator << 
        self.assertEqual(32, (_ << 2)(8))
        # operator >> 
        self.assertEqual(2, (_ >> 2)(8))
        # operator (-a)
        self.assertEqual(10,  (-_)(-10))
        self.assertEqual(-10, (-_)(10))
        # operator (+a)
        self.assertEqual(10,  (+_)(10))
        self.assertEqual(-10, (+_)(-10))
        # operator (~a)
        self.assertEqual(-11, (~_)(10))

    def test_arithmetic_multiple(self):
        self.assertEqual(10, (_ + _)(5, 5))
        self.assertEqual(0, (_ - _)(5, 5))
        self.assertEqual(25, (_ * _)(5, 5))
        self.assertEqual(1, (_ / _)(5, 5))

    def test_arithmetic_swap(self):
        # operator +
        self.assertEqual(7, (2 + _)(5))
        self.assertEqual([10,11,12], list(map(10 + _, [0,1,2])))
        # operator -
        self.assertEqual(3, (8 - _)(5))
        self.assertEqual(13, (8 - _ + 10)(5))
        self.assertEqual([10,9,8], list(map(10 - _, [0,1,2])))
        # operator * 
        self.assertEqual(10, (2 * _)(5))
        self.assertEqual(50, (2 * _ + 40)(5))
        self.assertEqual([0,10,20], list(map(10 * _, [0,1,2])))
        # operator /
        self.assertEqual(5, (10 / _)(2))
        self.assertEqual(6, (10 / _ + 1)(2))
        self.assertEqual([10,5,2], list(map(100 / _, [10,20,50])))
        # operator **
        self.assertEqual(100, (10**_)(2))
        # operator %
        self.assertEqual(1, (11 % _)(2))
        # operator << 
        self.assertEqual(32, (8 << _)(2))
        # operator >> 
        self.assertEqual(2, (8 >> _)(2))

    def test_bitwise(self):
        # and
        self.assertTrue( (_ & 1)(1))
        self.assertFalse((_ & 1)(0))
        self.assertFalse((_ & 0)(1))
        self.assertFalse((_ & 0)(0))
        # or 
        self.assertTrue( (_ | 1)(1))
        self.assertTrue( (_ | 1)(0))
        self.assertTrue( (_ | 0)(1))
        self.assertFalse((_ | 0)(0))
        # xor
        self.assertTrue( (_ ^ 1)(0))
        self.assertTrue( (_ ^ 0)(1))
        self.assertFalse((_ ^ 1)(1))
        self.assertFalse((_ ^ 0)(0))

    def test_bitwise_swap(self):
        # and
        self.assertTrue( (1 & _)(1))
        self.assertFalse((1 & _)(0))
        self.assertFalse((0 & _)(1))
        self.assertFalse((0 & _)(0))
        # or 
        self.assertTrue( (1 | _)(1))
        self.assertTrue( (1 | _)(0))
        self.assertTrue( (0 | _)(1))
        self.assertFalse((0 | _)(0))
        # xor
        self.assertTrue( (1 ^ _)(0))
        self.assertTrue( (0 ^ _)(1))
        self.assertFalse((1 ^ _)(1))
        self.assertFalse((0 ^ _)(0))

    def test_getattr(self):
        class GetattrTest(object):
            def __init__(self):
                self.doc = "TestCase"

        self.assertEqual("TestCase", (_.doc)(GetattrTest()))
        self.assertEqual("TestCaseTestCase", (_.doc * 2)(GetattrTest()))
        self.assertEqual("TestCaseTestCase", (_.doc + _.doc)(GetattrTest(), GetattrTest()))

    def test_call_method(self):
        self.assertEqual(["test", "case"], (_.call("split"))("test case"))
        self.assertEqual("str", _.__name__(str))

    def test_call_method_args(self):
        self.assertEqual(["test", "case"], (_.call("split", "-"))("test-case"))
        self.assertEqual(["test-case"], (_.call("split", "-", 0))("test-case"))

    def test_call_method_kwargs(self):
        test_dict = {'num': 23}
        _.call("update", num = 42)(test_dict)
        self.assertEqual({'num': 42}, (test_dict))

    def test_comparator(self):
        self.assertTrue((_ < 7)(1))
        self.assertFalse((_ < 7)(10))
        self.assertTrue((_ > 20)(25))
        self.assertFalse((_ > 20)(0))
        self.assertTrue((_ <= 7)(6))
        self.assertTrue((_ <= 7)(7))
        self.assertFalse((_ <= 7)(8))
        self.assertTrue((_ >= 7)(8))
        self.assertTrue((_ >= 7)(7))
        self.assertFalse((_ >= 7)(6))
        self.assertTrue((_ == 10)(10))
        self.assertFalse((_ == 10)(9))

    def test_none(self):
        self.assertTrue((_ == None)(None))

        class pushlist(list):
            def __lshift__(self, item):
                self.append(item)
                return self

        self.assertEqual([None], (_ << None)(pushlist()))

    def test_comparator_multiple(self):
        self.assertTrue((_ < _)(1, 2))
        self.assertFalse((_ < _)(2, 1))
        self.assertTrue((_ > _)(25, 20))
        self.assertFalse((_ > _)(20, 25))
        self.assertTrue((_ <= _)(6, 7))
        self.assertTrue((_ <= _)(7, 7))
        self.assertFalse((_ <= _)(8, 7))
        self.assertTrue((_ >= _)(8, 7))
        self.assertTrue((_ >= _)(7, 7))
        self.assertFalse((_ >= _)(6, 7))
        self.assertTrue((_ == _)(10, 10))
        self.assertFalse((_ == _)(9, 10))

    def test_comparator_filter(self):
        self.assertEqual([0,1,2], list(filter(_ < 5, [0,1,2,10,11,12])))

    def test_slicing(self):
        self.assertEqual(0,       (_[0])(list(range(10))))
        self.assertEqual(9,       (_[-1])(list(range(10))))
        self.assertEqual([3,4,5], (_[3:])(list(range(6))))
        self.assertEqual([0,1,2], (_[:3])(list(range(10))))
        self.assertEqual([1,2,3], (_[1:4])(list(range(10))))
        self.assertEqual([0,2,4], (_[0:6:2])(list(range(10))))

    def test_slicing_multiple(self):
        self.assertEqual(0, (_[_])(range(10), 0))
        self.assertEqual(8, (_[_ * (-1)])(range(10), 2))

    def test_arity_error(self):
        self.assertRaises(underscore.ArityError, _, 1, 2)
        self.assertRaises(underscore.ArityError, _ + _, 1)
        # can be catched as TypeError
        self.assertRaises(TypeError, _, 1, 2)
        self.assertRaises(TypeError, _ + _, 1)

    def test_more_than_2_operations(self):
        self.assertEqual(12, (_ * 2 + 10)(1))
        self.assertEqual(6,  (_ + _ + _)(1,2,3))
        self.assertEqual(10, (_ + _ + _ + _)(1,2,3,4))
        self.assertEqual(7,  (_ + _ * _)(1,2,3))

    def test_string_converting(self):
        self.assertEqual("(x1) => x1", str(_))

        self.assertEqual("(x1) => (x1 + 2)",  str(_ + 2))
        self.assertEqual("(x1) => (x1 - 2)",  str(_ - 2))
        self.assertEqual("(x1) => (x1 * 2)",  str(_ * 2))
        self.assertEqual("(x1) => (x1 / 2)",  str(_ / 2))
        self.assertEqual("(x1) => (x1 % 2)",  str(_ % 2))
        self.assertEqual("(x1) => (x1 ** 2)", str(_ ** 2))

        self.assertEqual("(x1) => (x1 & 2)", str(_ & 2))
        self.assertEqual("(x1) => (x1 | 2)", str(_ | 2))
        self.assertEqual("(x1) => (x1 ^ 2)", str(_ ^ 2))

        self.assertEqual("(x1) => (x1 >> 2)", str(_ >> 2))
        self.assertEqual("(x1) => (x1 << 2)", str(_ << 2))

        self.assertEqual("(x1) => (x1 < 2)",  str(_ < 2))
        self.assertEqual("(x1) => (x1 > 2)",  str(_ > 2))
        self.assertEqual("(x1) => (x1 <= 2)", str(_ <= 2))
        self.assertEqual("(x1) => (x1 >= 2)", str(_ >= 2))
        self.assertEqual("(x1) => (x1 == 2)", str(_ == 2))
        self.assertEqual("(x1) => (x1 != 2)", str(_ != 2))

    def test_rigthside_string_converting(self):
        self.assertEqual("(x1) => (2 + x1)",  str(2 + _))
        self.assertEqual("(x1) => (2 - x1)",  str(2 - _))
        self.assertEqual("(x1) => (2 * x1)",  str(2 * _))
        self.assertEqual("(x1) => (2 / x1)",  str(2 / _))
        self.assertEqual("(x1) => (2 % x1)",  str(2 % _))
        self.assertEqual("(x1) => (2 ** x1)", str(2 ** _))

        self.assertEqual("(x1) => (2 & x1)", str(2 & _))
        self.assertEqual("(x1) => (2 | x1)", str(2 | _))
        self.assertEqual("(x1) => (2 ^ x1)", str(2 ^ _))

        self.assertEqual("(x1) => (2 >> x1)", str(2 >> _))
        self.assertEqual("(x1) => (2 << x1)", str(2 << _))

    def test_unary_string_converting(self):
        self.assertEqual("(x1) => (+x1)", str(+_))
        self.assertEqual("(x1) => (-x1)", str(-_))
        self.assertEqual("(x1) => (~x1)", str(~_))

    def test_multiple_string_converting(self):
        self.assertEqual("(x1, x2) => (x1 + x2)", str(_ + _))
        self.assertEqual("(x1, x2) => (x1 * x2)", str(_ * _))
        self.assertEqual("(x1, x2) => (x1 - x2)", str(_ - _))
        self.assertEqual("(x1, x2) => (x1 / x2)", str(_ / _))
        self.assertEqual("(x1, x2) => (x1 % x2)", str(_ % _))
        self.assertEqual("(x1, x2) => (x1 ** x2)", str(_ ** _))

        self.assertEqual("(x1, x2) => (x1 & x2)", str(_ & _))
        self.assertEqual("(x1, x2) => (x1 | x2)", str(_ | _))
        self.assertEqual("(x1, x2) => (x1 ^ x2)", str(_ ^ _))

        self.assertEqual("(x1, x2) => (x1 >> x2)", str(_ >> _))
        self.assertEqual("(x1, x2) => (x1 << x2)", str(_ << _))

        self.assertEqual("(x1, x2) => (x1 > x2)",  str(_ > _))
        self.assertEqual("(x1, x2) => (x1 < x2)",  str(_ < _))
        self.assertEqual("(x1, x2) => (x1 >= x2)", str(_ >= _))
        self.assertEqual("(x1, x2) => (x1 <= x2)", str(_ <= _))
        self.assertEqual("(x1, x2) => (x1 == x2)", str(_ == _))
        self.assertEqual("(x1, x2) => (x1 != x2)", str(_ != _))

    def test_reverse_string_converting(self):
        self.assertEqual("(x1, x2, x3) => ((x1 + x2) + x3)", str(_ + _ + _))
        self.assertEqual("(x1, x2, x3) => (x1 + (x2 * x3))", str(_ + _ * _))

    def test_multi_underscore_string_converting(self):
        self.assertEqual("(x1) => (x1 + '_')", str(_ + "_"))
        self.assertEqual("(x1, x2) => getattr((x1 + x2), '__and_now__')", str((_ + _).__and_now__))
        self.assertEqual("(x1, x2) => x1['__name__'][x2]", str(_['__name__'][_]))

    def test_repr(self):
        self.assertEqual(_ / 2, eval(repr(_ / 2)))
        self.assertEqual(_ + _, eval(repr(_ + _)))
        self.assertEqual(_ + _ * _, eval(repr(_ + _ * _)))

class CompositionTestCase(unittest.TestCase):

    def test_composition(self):
        def f(x): return x * 2
        def g(x): return x + 10

        self.assertEqual(30, (F(f) << g)(5))

        def z(x): return x * 20
        self.assertEqual(220, (F(f) << F(g) << F(z))(5))

    def test_partial(self):
        # Partial should work if we pass additional arguments to F constructor
        f = F(operator.add, 10) << F(operator.add, 5)
        self.assertEqual(25, f(10))

    def test_underscore(self):
        self.assertEqual([1, 4, 9], list(map(F() << (_ ** 2) << _ + 1, range(3))))    

    def test_pipe_composition(self):
        def f(x): return x * 2
        def g(x): return x + 10

        self.assertEqual(20, (F() >> f >> g)(5))

    def test_pipe_partial(self):
        func = F() >> (iters.filter, _ < 6) >> sum
        self.assertEqual(15, func(iters.range(10)))

class IteratorsTestCase(unittest.TestCase):

    def test_take(self):
        self.assertEqual([0,1], list(iters.take(2, range(10))))
        self.assertEqual([0,1], list(iters.take(10, range(2))))

    def test_drop(self):
        self.assertEqual([3,4], list(iters.drop(3, range(5))))
        self.assertEqual([], list(iters.drop(10, range(2))))

    def test_takelast(self):
        self.assertEqual([8,9], list(iters.takelast(2, range(10))))
        self.assertEqual([0,1], list(iters.takelast(10, range(2))))

    def test_droplast(self):
        self.assertEqual([0,1], list(iters.droplast(3, range(5))))
        self.assertEqual([], list(iters.droplast(10, range(2))))

    def test_consume(self):
        # full consuming, without limitation
        r = iters.range(10)
        self.assertEqual(10, len(list(r)))
        itr = iter(r)
        iters.consume(itr)
        self.assertEqual(0, len(list(itr)))

    def test_consume_limited(self):
        r = iters.range(10)
        self.assertEqual(10, len(list(r)))
        itr = iter(r)
        iters.consume(itr, 5)
        self.assertEqual(5, len(list(itr)))

    def test_nth(self):
        self.assertEqual(1, iters.nth(range(5), 1))
        self.assertEqual(None, iters.nth(range(5), 10))
        self.assertEqual("X", iters.nth(range(5), 10, "X"))

    def test_head(self):
        self.assertEqual(0, iters.head([0,1,2]))
        self.assertEqual(None, iters.head([]))

        def gen():
            yield 1 
            yield 2
            yield 3 

        self.assertEqual(1, iters.head(gen()))

    def test_tail(self):
        self.assertEqual([1,2], list(iters.tail([0,1,2])))
        self.assertEqual([], list(iters.tail([])))

        def gen():
            yield 1 
            yield 2
            yield 3 

        self.assertEqual([2,3], list(iters.tail(gen())))

    def test_compact(self):
        self.assertEqual([True, 1, 0.1, "non-empty", [""], (0,), {"a": 1}],
                         list(iters.compact([None, False, True, 0, 1, 0.0, 0.1,
                                             "", "non-empty", [], [""],
                                             (), (0,), {}, {"a": 1}])))

    def test_reject(self):
        self.assertEqual([1, 3, 5, 7, 9],
                         list(iters.reject(_ % 2 == 0, range(1, 11))))
        self.assertEqual([None, False, 0, 0.0, "", [], (), {}],
                         list(iters.reject(None, [None, False, True, 0, 1,
                                                  0.0, 0.1, "", "non-empty",
                                                  [], [""], (), (0,),
                                                  {}, {"a": 1}])))

    def test_padnone(self):
        it = iters.padnone([10,11])
        self.assertEqual(10, next(it))
        self.assertEqual(11, next(it))
        self.assertEqual(None, next(it))
        self.assertEqual(None, next(it))

    def test_ncycles(self):
        it = iters.ncycles([10,11], 2)
        self.assertEqual(10, next(it))
        self.assertEqual(11, next(it))
        self.assertEqual(10, next(it))
        self.assertEqual(11, next(it))
        self.assertRaises(StopIteration, next, it)

    def test_repeatfunc(self):
        def f():
            return "test"

        # unlimited count
        it = iters.repeatfunc(f)
        self.assertEqual("test", next(it))
        self.assertEqual("test", next(it))
        self.assertEqual("test", next(it))

        # limited
        it = iters.repeatfunc(f, 2)
        self.assertEqual("test", next(it))
        self.assertEqual("test", next(it))
        self.assertRaises(StopIteration, next, it)

    def test_grouper(self):
        # without fill value (default should be None)
        a, b, c = iters.grouper(3, "ABCDEFG")
        self.assertEqual(["A","B","C"], list(a))
        self.assertEqual(["D","E","F"], list(b))
        self.assertEqual(["G",None,None], list(c))

        # with fill value
        a, b, c = iters.grouper(3, "ABCDEFG", "x")
        self.assertEqual(["A","B","C"], list(a))
        self.assertEqual(["D","E","F"], list(b))
        self.assertEqual(["G","x","x"], list(c))

    def test_roundrobin(self):
        r = iters.roundrobin('ABC', 'D', 'EF')
        self.assertEqual(["A","D","E","B","F","C"], list(r))

    def test_partition(self):
        def is_odd(x):
            return x % 2 == 1

        before, after = iters.partition(is_odd, iters.range(5))
        self.assertEqual([0,2,4], list(before))
        self.assertEqual([1,3], list(after))

    def test_splitat(self):
        before, after = iters.splitat(2, iters.range(5))
        self.assertEqual([0,1], list(before))
        self.assertEqual([2,3,4], list(after))

    def test_splitby(self):
        def is_even(x):
            return x % 2 == 0

        before, after = iters.splitby(is_even, iters.range(5))
        self.assertEqual([0], list(before))
        self.assertEqual([1, 2,3,4], list(after))

    def test_powerset(self):
        ps = iters.powerset([1,2])
        self.assertEqual([tuple(),(1,),(2,),(1,2)], list(ps))

    def test_pairwise(self):
        ps = iters.pairwise([1,2,3,4])
        self.assertEqual([(1,2),(2,3),(3,4)], list(ps))

    def test_iter_except(self):
        d = ["a", "b", "c"]
        it = iters.iter_except(d.pop, IndexError)
        self.assertEqual(["c", "b", "a"], list(it))

    def test_flatten(self):
        # flatten nested lists
        self.assertEqual([1,2,3,4], list(iters.flatten([[1,2], [3,4]])))
        self.assertEqual([1,2,3,4,5,6], list(iters.flatten([[1,2], [3, [4,5,6]]])))
        # flatten nested tuples, sets, and frozen sets
        self.assertEqual([1,2,3,4,5,6], list(iters.flatten(((1,2), (3, (4,5,6))))))
        self.assertEqual([1,2,3], list(iters.flatten(set([1, frozenset([2,3])]))))
        # flatten nested generators
        generators = ((num + 1 for num in range(0, n)) for n in range(1, 4))
        self.assertEqual([1,1,2,1,2,3], list(iters.flatten(generators)))
        # flat list should return itself
        self.assertEqual([1,2,3], list(iters.flatten([1,2,3])))
        # Don't flatten strings, bytes, or bytearrays
        self.assertEqual([2,"abc",1], list(iters.flatten([2,"abc",1])))
        self.assertEqual([2, b'abc', 1], list(iters.flatten([2, b'abc', 1])))
        self.assertEqual([2, bytearray(b'abc'), 1], 
                         list(iters.flatten([2, bytearray(b'abc'), 1])))

    def test_accumulate(self):
        self.assertEqual([1,3,6,10,15], list(iters.accumulate([1,2,3,4,5])))
        self.assertEqual([1,2,6,24,120], list(iters.accumulate([1,2,3,4,5], operator.mul)))

    def test_filterfalse(self):
        l = iters.filterfalse(lambda x: x > 10, [1,2,3,11,12])
        self.assertEqual([1,2,3], list(l))

class StreamTestCase(unittest.TestCase):

    def test_from_list(self):
        s = Stream() << [1,2,3,4,5]
        self.assertEqual([1,2,3,4,5], list(s))
        self.assertEqual(2, s[1])
        self.assertEqual([1,2], list(s[0:2]))

    def test_from_iterator(self):
        s = Stream() << range(6) << [6,7]
        self.assertEqual([0,1,2,3,4,5,6,7], list(s))

    def test_from_generator(self):
        def gen():
            yield 1
            yield 2
            yield 3
        
        s = Stream() << gen << (4,5)
        assert list(s) == [1,2,3,4,5]

    def test_lazy_slicing(self):
        s = Stream() << iters.range(10)
        self.assertEqual(s.cursor(), 0)

        s_slice = s[:5]
        self.assertEqual(s.cursor(), 0)
        self.assertEqual(len(list(s_slice)), 5)

    def test_lazy_slicing_recursive(self):
        s = Stream() << iters.range(10)
        sf = s[1:3][0:2]

        self.assertEqual(s.cursor(), 0)
        self.assertEqual(len(list(sf)), 2)

    def test_fib_infinite_stream(self):
        from operator import add 

        f = Stream()
        fib = f << [0, 1] << iters.map(add, f, iters.drop(1, f))

        self.assertEqual([0,1,1,2,3,5,8,13,21,34], list(iters.take(10, fib)))
        self.assertEqual(6765, fib[20])
        self.assertEqual([832040,1346269,2178309,3524578,5702887], list(fib[30:35]))
        # 35 elements should be already evaluated
        self.assertEqual(fib.cursor(), 35)

    def test_origin_param(self):
        self.assertEqual([100], list(Stream(100)))
        self.assertEqual([1,2,3], list(Stream(1, 2, 3)))
        self.assertEqual([1,2,3,10,20,30], list(Stream(1, 2, 3) << [10,20,30]))

    def test_origin_param_string(self):
        self.assertEqual(["stream"], list(Stream("stream")))

class OptionTestCase(unittest.TestCase, InstanceChecker):

    def test_create_option(self):
        self.assertIsInstance(monad.Option("A"), monad.Full)
        self.assertIsInstance(monad.Option(10), monad.Full)
        self.assertIsInstance(monad.Option(10, lambda x: x > 7), monad.Full)
        self.assertIsInstance(monad.Option(None), monad.Empty)
        self.assertIsInstance(monad.Option(False), monad.Full)
        self.assertIsInstance(monad.Option(0), monad.Full)
        self.assertIsInstance(monad.Option(False, checker=bool), monad.Empty)
        self.assertIsInstance(monad.Option(0, checker=bool), monad.Empty)
        self.assertIsInstance(monad.Option(10, lambda x: x > 70), monad.Empty)

    def test_map_filter(self):
        class Request(dict):
            def parameter(self, name):
                return monad.Option(self.get(name, None))

        r = Request(testing="Fixed", empty="   ")

        # full chain
        self.assertEqual("FIXED", r.parameter("testing")
                                   .map(operator.methodcaller("strip"))
                                   .filter(len)
                                   .map(operator.methodcaller("upper"))
                                   .get_or(""))

        # breaks on filter
        self.assertEqual("", r.parameter("empty")
                              .map(operator.methodcaller("strip"))
                              .filter(len)
                              .map(operator.methodcaller("upper"))
                              .get_or(""))

        # breaks on parameter
        self.assertEqual("", r.parameter("missed")
                              .map(operator.methodcaller("strip"))
                              .filter(len)
                              .map(operator.methodcaller("upper"))
                              .get_or(""))

    def test_empty_check(self):
        self.assertTrue(monad.Empty().empty)
        self.assertTrue(monad.Option(None).empty)
        self.assertTrue(monad.Option.from_call(lambda: None).empty)
        self.assertFalse(monad.Option(10).empty)
        self.assertFalse(monad.Full(10).empty)

    def test_lazy_orcall(self):
        def from_mimetype(request):
            # you can return both value or Option
            return request.get("mimetype", None)

        def from_extension(request):
            # you can return both value or Option
            return monad.Option(request.get("url", None))\
                        .map(lambda s: s.split(".")[-1])

        # extract value from extension
        r = dict(url="myfile.png")
        self.assertEqual("PNG", monad.Option(r.get("type", None)) \
                                     .or_call(from_mimetype, r) \
                                     .or_call(from_extension, r) \
                                     .map(operator.methodcaller("upper")) \
                                     .get_or(""))

        # extract value from mimetype
        r = dict(url="myfile.svg", mimetype="png")
        self.assertEqual("PNG", monad.Option(r.get("type", None)) \
                                     .or_call(from_mimetype, r) \
                                     .or_call(from_extension, r) \
                                     .map(operator.methodcaller("upper")) \
                                     .get_or(""))

        # type is set directly
        r = dict(url="myfile.jpeg", mimetype="svg", type="png")
        self.assertEqual("PNG", monad.Option(r.get("type", None)) \
                                     .or_call(from_mimetype, r) \
                                     .or_call(from_extension, r) \
                                     .map(operator.methodcaller("upper")) \
                                     .get_or(""))

    def test_optionable_decorator(self):
        class Request(dict):
            @monad.optionable
            def parameter(self, name):
                return self.get(name, None)

        r = Request(testing="Fixed", empty="   ")

        # full chain
        self.assertEqual("FIXED", r.parameter("testing")
                                   .map(operator.methodcaller("strip"))
                                   .filter(len)
                                   .map(operator.methodcaller("upper"))
                                   .get_or(""))

    def test_stringify(self):
        self.assertEqual("Full(10)", str(monad.Full(10)))
        self.assertEqual("Full(in box!)", str(monad.Full("in box!")))
        self.assertEqual("Empty()", str(monad.Empty()))
        self.assertEqual("Empty()", str(monad.Option(None)))

    def test_option_repr(self):
        self.assertEqual("Full(10)", repr(monad.Full(10)))
        self.assertEqual("Full(in box!)", repr(monad.Full("in box!")))
        self.assertEqual("Empty()", repr(monad.Empty()))
        self.assertEqual("Empty()", repr(monad.Option(None)))

    def test_static_constructor(self):
        self.assertEqual(monad.Empty(),  monad.Option.from_value(None))
        self.assertEqual(monad.Full(10), monad.Option.from_value(10))
        self.assertEqual(monad.Empty(),  monad.Option.from_call(lambda: None))
        self.assertEqual(monad.Full(10), monad.Option.from_call(operator.add, 8, 2))
        self.assertEqual(monad.Empty(), 
                         monad.Option.from_call(lambda d, k: d[k], 
                                                {"a":1}, "b", exc=KeyError))

    def test_flatten_operation(self):
        self.assertEqual(monad.Empty(), monad.Empty(monad.Empty()))
        self.assertEqual(monad.Empty(), monad.Empty(monad.Full(10)))
        self.assertEqual(monad.Empty(), monad.Full(monad.Empty()))
        self.assertEqual("Full(20)", str(monad.Full(monad.Full(20))))

class TrampolineTestCase(unittest.TestCase):

    def test_tco_decorator(self):

        def recur_accumulate(origin, f=operator.add, acc=0):
            n = next(origin, None)
            if n is None: return acc
            return recur_accumulate(origin, f, f(acc, n))

        # this works normally
        self.assertEqual(10, recur_accumulate(iter(range(5))))

        limit = sys.getrecursionlimit() * 10
        # such count of recursive calls should fail on CPython,
        # for PyPy we skip this test cause on PyPy the limit is
        # approximative and checked at a lower level
        if not hasattr(sys, 'pypy_version_info'):
            self.assertRaises(RuntimeError, recur_accumulate, iter(range(limit)))

        # with recur decorator it should run without problems
        @recur.tco
        def tco_accumulate(origin, f=operator.add, acc=0):
            n = next(origin, None)
            if n is None: return False, acc
            return True, (origin, f, f(acc, n))

        self.assertEqual(sum(range(limit)), tco_accumulate(iter(range(limit))))

    def test_tco_different_functions(self):

        @recur.tco
        def recur_inc2(curr, acc=0):
            if curr == 0: return False, acc
            return recur_dec, (curr-1, acc+2)

        @recur.tco
        def recur_dec(curr, acc=0):
            if curr == 0: return False, acc
            return recur_inc2, (curr-1, acc-1)

        self.assertEqual(5000, recur_inc2(10000))

if __name__ == '__main__':
    unittest.main()
