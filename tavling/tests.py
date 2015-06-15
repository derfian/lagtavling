"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from tavling.models import SortableResult, Resultat
import operator


class SortableResultTestCase(TestCase):
    def setUp(self):
        self.base = SortableResult(1, 5.0, False)
        self.equal = SortableResult(1, 5.0, False)

        self.greaters = [SortableResult(1, 6.0, False),
                         SortableResult(2, 5.0, False),
                         SortableResult(2, 4.0, False),
                         SortableResult(None, None, True)]

        self.lessers = [SortableResult(1, 4.0, False),
                        SortableResult(0, 5.0, False),
                        SortableResult(0, 10.0, False)]

        self.incompletes = [SortableResult(None, None, False),
                            SortableResult(None, None, False)]

        self.disqualifieds = [SortableResult(None, None, True),
                              SortableResult(None, None, True)]

    def test_equal(self):
        self.assertEqual(self.base, self.equal)

        # All incompletes are equal to each other
        candidate = self.incompletes[0]
        for incomplete in self.incompletes:
            self.assertEqual(candidate, incomplete)

        # All disqualifies are equal to each other
        candidate = self.disqualifieds[0]
        for disq in self.disqualifieds:
            self.assertEqual(candidate, disq)


    def test_not_equal(self):
        for n in self.greaters + self.lessers + self.incompletes + self.disqualifieds:
            self.assertNotEqual(self.base, n,
                                "%s is equal to %s" % (n, self.base))

    def test_gt(self):
        for n in self.greaters:
            self.assertTrue(n > self.base,
                            "%s is not greater than %s" % (n, self.base))
            self.assertFalse(n > self.incompletes[0])
            self.assertFalse(n > self.disqualifieds[0])

    def test_lt(self):
        for n in self.lessers:
            self.assertTrue(n < self.base,
                            "%s is not less than %s" % (n, self.base))
            self.assertTrue(n < self.incompletes[0])
            self.assertTrue(n < self.disqualifieds[0])

    def test_le(self):
        for n in self.lessers + [self.equal]:
            self.assertTrue(n <= self.base,
                            "%s is not lesser or equal to %s" % (n, self.base))

    def test_ge(self):
        for n in self.greaters + [self.equal]:
            self.assertTrue(n >= self.base,
                            "%s is not greater or equal to %s" % (n, self.base))

