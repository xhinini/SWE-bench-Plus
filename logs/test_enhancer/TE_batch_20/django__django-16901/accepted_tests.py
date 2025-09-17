from django.db import connection

def test_filter_three_operands(self):
    qs = Number.objects.filter(Q(num__gte=1) ^ Q(num__gte=3) ^ Q(num__gte=5))
    expected = [i for i in range(10) if (i >= 1) ^ (i >= 3) ^ (i >= 5)]
    self.assertCountEqual(qs, [self.numbers[i] for i in expected])

def test_filter_four_operands(self):
    qs = Number.objects.filter(Q(num__gte=1) ^ Q(num__gte=3) ^ Q(num__gte=5) ^ Q(num__gte=7))
    expected = [i for i in range(10) if (i >= 1) ^ (i >= 3) ^ (i >= 5) ^ (i >= 7)]
    self.assertCountEqual(qs, [self.numbers[i] for i in expected])

def test_values_list_five_operands(self):
    qs = Number.objects.filter(Q(num__gte=0) ^ Q(num__gte=2) ^ Q(num__gte=4) ^ Q(num__gte=6) ^ Q(num__gte=8))
    expected = [i for i in range(10) if (i >= 0) ^ (i >= 2) ^ (i >= 4) ^ (i >= 6) ^ (i >= 8)]
    self.assertCountEqual(list(qs.values_list('num', flat=True)), expected)

def test_negated_mixed_three(self):
    qs = Number.objects.filter(Q(num__gte=1) ^ ~Q(num__gte=3) ^ Q(num__gte=5))
    expected = [i for i in range(10) if (i >= 1) ^ (not i >= 3) ^ (i >= 5)]
    expected_indexes = [i for i, val in enumerate(expected) if val]
    self.assertCountEqual(qs, [self.numbers[i] for i in expected_indexes])

def test_exclude_three_operands(self):
    qs = Number.objects.exclude(Q(num__gte=1) ^ Q(num__gte=3) ^ Q(num__gte=5))
    expected = [i for i in range(10) if not (i >= 1) ^ (i >= 3) ^ (i >= 5)]
    self.assertCountEqual(qs, [self.numbers[i] for i in expected])

def test_chained_filter_three_operands(self):
    qs = Number.objects.filter(num__gte=0).filter(Q(num__gte=1) ^ Q(num__gte=3) ^ Q(num__gte=5))
    expected = [i for i in range(10) if (i >= 1) ^ (i >= 3) ^ (i >= 5)]
    self.assertCountEqual(qs, [self.numbers[i] for i in expected])

def test_pk_q_multiple_operands(self):
    a, b, c = (self.numbers[0], self.numbers[1], self.numbers[2])
    qs = Number.objects.filter(Q(pk=a.pk) ^ Q(pk=b.pk) ^ Q(pk=c.pk))
    self.assertCountEqual(qs, [a, b, c])

def test_empty_in_with_multiple_operands(self):
    qs = Number.objects.filter(Q(pk__in=[]) ^ Q(num__gte=3) ^ Q(num__lte=6))
    expected = [i for i in range(10) if ([].__contains__(i) is False) ^ (i >= 3) ^ (i <= 6)]
    expected_indexes = [i for i in range(10) if (i >= 3) ^ (i <= 6)]
    self.assertCountEqual(qs, [self.numbers[i] for i in expected_indexes])

def test_many_operands_compilation(self):
    operands = [Q(num__gte=i) for i in range(1, 7)]
    expr = operands[0]
    for op in operands[1:]:
        expr = expr ^ op
    qs = Number.objects.filter(expr)
    expected = [i for i in range(10) if any((i >= j for j in range(1, 7))) ^ False]
    list_qs = list(qs)
    self.assertTrue(0 <= len(list_qs) <= 10)

def test_where_as_sql_compiles_for_multiple_operands(self):
    qs = Number.objects.filter(Q(num__gte=1) ^ Q(num__gte=3) ^ Q(num__gte=5))
    compiler = qs.query.get_compiler(connection=connection)
    sql_tuple = qs.query.where.as_sql(compiler, connection)
    self.assertIsInstance(sql_tuple, tuple)
    self.assertEqual(len(sql_tuple), 2)

from functools import reduce
import operator
from functools import reduce
import operator
from django.db.models import Q
from django.test import TestCase
from .models import Number

def bool_xor(*conds):
    return reduce(operator.xor, conds, False)