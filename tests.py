#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for Fn.py library"""

import unittest

from fn import operator as op
from fn import _

class OperatorTestCase(unittest.TestCase):
    def test_currying(self):
    	def add(first):
    		def add(second):
    			return first + second
    		return add

    	self.assertEqual(1, op.curry(add, 0, 1))

class UnderscoreTestCase(unittest.TestCase):
	def test_add_single(self):
		self.assertEqual(7, (_ + 2)(5))
		self.assertEqual([10,11,12], list(map(_ + 10, range(3))))
		self.assertEqual(10, (_ + _)(5, 5))

	def test_mul(self):
		self.assertEqual(10, (_ * 2)(5))
		self.assertEqual(50, (_ * 2 + 40)(5))
		self.assertEqual(25, (_ * _)(5, 5))

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

	def test_comparator_single(self):
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

	def test_slicing_single(self):
		self.assertEqual(0, 	  (_[0])(range(10)))
		self.assertEqual(9, 	  (_[-1])(range(10)))
		self.assertEqual([3,4,5], (_[3:])(range(6)))
		self.assertEqual([0,1,2], (_[:3])(range(10)))
		self.assertEqual([1,2,3], (_[1:4])(range(10)))
		self.assertEqual([0,2,4], (_[0:6:2])(range(10)))

	def test_slicing_multiple(self):
		self.assertEqual(0, (_[_])(range(10), 0))
		self.assertEqual(8, (_[_ * (-1)])(range(10), 2))
