# -*- mode: python; coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from tavling.utils import *
from tavling.models import Result, Contestant, IndividualStart

class AddResultsTestCase(TestCase):
    def test_add_two_results(self):
        a = (0, 5.0, False)
        b = (0, 10.0, False)
        c = (5, 5.0, False)
        d = (5, 10.0, False)
        e = (0, 10.0, True)
        f = (None, None, True)
        self.assertEqual(add_results(a,b), (0, 15.0, False))
        self.assertEqual(add_results(a,c), (5, 10.0, False))
        self.assertEqual(add_results(a,d), (5, 15.0, False))
        self.assertEqual(add_results(a,e), (None, None, True))
        self.assertEqual(add_results(a,f), (None, None, True))

class CombineResultsTestCase(TestCase):

    # Less than three valid results → None

    def test_incomplete(self):
        # valid, 3 × incomplete
        r = [(1, 2, False), None, None, None]
        self.assertEqual(combine_results(r), None)

        # 2 × valid, 2 × incomplete
        r = [(1, 2, False), (2, 3, False), None, None]
        self.assertEqual(combine_results(r), None)

    # Less than three valid+incomplete results → disqualified

    def test_disqualified(self):
        # 2 × disqualified, 2 × incomplete
        r = [(None, None, True), (None, None, True), None, None]
        self.assertEqual(combine_results(r), (None, None, True))

        # Too few results results in disqualified no matter what
        r = [None, None]
        self.assertEqual(combine_results(r), (None, None, True))

    def test_three_valid(self):
        # Three valids
        r = [(0, 10, False), (1, 11, False), (2, 12, False)]
        self.assertEqual(combine_results(r), (3, 33, False))

        # With a fourth incomplete
        r = [(0, 10, False), (1, 11, False), (2, 12, False), None]
        self.assertEqual(combine_results(r), (3, 33, False))

        # With a fourth disqualification
        r = [(0, 10, False), (1, 11, False), (2, 12, False), (None, None, True)]
        self.assertEqual(combine_results(r), (3, 33, False))

    def test_four_valid(self):
        # Make sure only the three best results are selected.
        r = [(0, 10, False),
             (1, 11, False),
             (2, 12, False),
             (3, 13, False)]
        self.assertEqual(combine_results(r),
                         (3, 33, False))

        r = [(0, 10, False),
             (0, 10, False),
             (0, 10, False),
             (3, 13, False)]
        self.assertEqual(combine_results(r),
                         (0, 30, False))

        r = [(0, 30, False),
             (0, 30, False),
             (0, 30, False),
             (3, 10, False)]
        self.assertEqual(combine_results(r),
                         (0, 90, False))

class SortFuncTupleTestCase(TestCase):
    def setUp(self):
        pass

    def test_sort_results_over_incomplete(self):
        a = (0, 10.0, False)
        b = None
        self.assertEqual(sorted([a, b], key=sortfunc_tuple)[0], a)
        self.assertEqual(sorted([b, a], key=sortfunc_tuple)[0], a)

    def test_sort_results_over_disqualified(self):
        a = (0, 10.0, False)
        b = (0, 10.0, True)
        self.assertEqual(sorted([a, b], key=sortfunc_tuple)[0], a)
        self.assertEqual(sorted([b, a], key=sortfunc_tuple)[0], a)

    def test_sort_disqualified_over_incomplete(self):
        a = None
        b = (0, 10.0, True)
        self.assertEqual(sorted([a, b], key=sortfunc_tuple)[0], b)
        self.assertEqual(sorted([b, a], key=sortfunc_tuple)[0], b)

# FIXME: Set up two contestants and two teams with results and compare
#        them, the following is wrong.
#
class SortFuncObjectTestCase(TestCase):
    def setUp(self):
        self.c1 = Contestant.objects.create(handler='Test1 Testsson', dog='Vov1 vovvson')
        self.c2 = Contestant.objects.create(handler='Test2 Testsson', dog='Vov2 vovvson')

        self.i1 = IndividualStart.objects.create(contestant=self.c1,
                                                order=1,
                                                size='S',
                                                jumping_result=None,
                                                agility_result=None)

        self.i2 = IndividualStart.objects.create(contestant=self.c2,
                                                order=2,
                                                size='S',
                                                jumping_result=None,
                                                agility_result=None)

    def test_sort_results_over_incomplete(self):
        self.rc = Result.objects.create(penalties=0, time='10.0', disqualified=False)
        #self.rd = Result.objects.create(penalties=None, time=None, disqualified=True)

        # Set results
        self.i1.jumping_result = self.rc
        self.i1.agility_result = self.rc
        self.i1.save()

        self.i2.jumping_result = None
        self.i2.agility_result = None
        self.i2.save()

        self.assertEqual(sorted([self.i1, self.i2], key=sortfunc_object)[0], self.i1)
        self.assertEqual(sorted([self.i2, self.i1], key=sortfunc_object)[0], self.i1)

    def test_sort_results_over_disqualified(self):
        self.rc = Result.objects.create(penalties=0, time='10.0', disqualified=False)
        self.rd = Result.objects.create(penalties=None, time=None, disqualified=True)

        # Set results
        self.i1.jumping_result = self.rc
        self.i1.agility_result = self.rc
        self.i1.save()

        self.i2.jumping_result = self.rd
        self.i2.agility_result = self.rd
        self.i2.save()

        self.assertEqual(sorted([self.i1, self.i2], key=sortfunc_object)[0], self.i1)
        self.assertEqual(sorted([self.i2, self.i1], key=sortfunc_object)[0], self.i1)

    def test_sort_results(self):
        self.rc1 = Result.objects.create(penalties=0, time='10.0', disqualified=False)
        self.rc2 = Result.objects.create(penalties=0, time='15.0', disqualified=False)

        # Set results
        self.i1.jumping_result = self.rc1
        self.i1.agility_result = self.rc1
        self.i1.save()

        self.i2.jumping_result = self.rc1
        self.i2.agility_result = self.rc2
        self.i2.save()

        self.assertEqual(sorted([self.i1, self.i2], key=sortfunc_object)[0], self.i1)
        self.assertEqual(sorted([self.i2, self.i1], key=sortfunc_object)[0], self.i1)
