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