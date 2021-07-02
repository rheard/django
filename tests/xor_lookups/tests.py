from operator import attrgetter

from django.db.models import Q
from django.test import TestCase

from .models import Number


class XorLookupsTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.numbers = {i: Number.objects.create(num=i) for i in range(1, 11)}

    def test_filter_xor(self):
        self.assertQuerysetEqual(
            (
                Number.objects.filter(num__lte=7) ^
                Number.objects.filter(num__gte=3)
            ), [
                1, 2, 8, 9, 10,
            ],
            attrgetter('num')
        )

        self.assertQuerysetEqual(
            Number.objects.filter(Q(num__lte=7) ^ Q(num__gte=3)), [
                1, 2, 8, 9, 10,
            ],
            attrgetter('num')
        )

    def test_stages(self):
        # You can shorten this syntax with code like the following,  which is
        # especially useful if building the query in stages:
        numbers = Number.objects.all()
        self.assertQuerysetEqual(
            numbers.filter(num__gte=0) ^ numbers.filter(num__lte=100),
            []
        )
        self.assertQuerysetEqual(
            numbers.filter(num__gte=0) ^ numbers.filter(num__lte=9), [
                10,
            ],
            attrgetter('num')
        )

    def test_pk_q(self):
        self.assertQuerysetEqual(
            Number.objects.filter(Q(pk=self.numbers[1].pk) ^ Q(pk=self.numbers[2].pk)), [
                1, 2,
            ],
            attrgetter('num')
        )

    def test_q_negated(self):
        # Q objects can be negated
        self.assertQuerysetEqual(
            Number.objects.filter(Q(num__lte=7) ^ ~Q(num__lt=3)), [
                1, 2, 8, 9, 10,
            ],
            attrgetter('num')
        )

    def test_empty_in(self):
        # Passing "in" an empty list returns no results ...
        self.assertQuerysetEqual(
            Number.objects.filter(pk__in=[]),
            []
        )
        # ... but can return results if we OR it with another query.
        self.assertQuerysetEqual(
            Number.objects.filter(Q(pk__in=[]) | Q(num__gte=5)), [
                5, 6, 7, 8, 9, 10,
            ],
            attrgetter('num'),
        )
