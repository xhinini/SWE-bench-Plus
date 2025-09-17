def test_avg_distinct_aggregate_returns_expected_value(self):
    vals = Book.objects.aggregate(avg_rating=Avg('rating', distinct=True))
    self.assertEqual(vals['avg_rating'], Approximate(4.125, places=3))

def test_sum_distinct_aggregate_returns_expected_value(self):
    vals = Book.objects.aggregate(sum_rating=Sum('rating', distinct=True))
    self.assertEqual(vals['sum_rating'], Approximate(Decimal('16.5'), places=3))

def test_avg_distinct_sql_contains_distinct(self):
    with CaptureQueriesContext(connection) as captured:
        Book.objects.aggregate(avg_rating=Avg('rating', distinct=True))
    self.assertGreaterEqual(len(captured.captured_queries), 1)
    sql = captured.captured_queries[0]['sql'].lower()
    self.assertIn('distinct', sql)

def test_sum_distinct_sql_contains_distinct(self):
    with CaptureQueriesContext(connection) as captured:
        Book.objects.aggregate(sum_rating=Sum('rating', distinct=True))
    self.assertGreaterEqual(len(captured.captured_queries), 1)
    sql = captured.captured_queries[0]['sql'].lower()
    self.assertIn('distinct', sql)

def test_annotate_avg_distinct_on_related_field(self):
    qs = Book.objects.annotate(distinct_authors_age_avg=Avg('authors__age', distinct=True))
    b4 = qs.get(pk=self.b4.pk)
    self.assertEqual(b4.distinct_authors_age_avg, Approximate(30.3333, places=3))

def test_annotate_sum_distinct_on_related_field(self):
    qs = Book.objects.annotate(distinct_authors_age_sum=Sum('authors__age', distinct=True))
    b1 = qs.get(pk=self.b1.pk)
    self.assertEqual(b1.distinct_authors_age_sum, 69)

def test_avg_distinct_duration_field(self):
    vals = Publisher.objects.aggregate(avg_duration=Avg('duration', distinct=True))
    self.assertEqual(vals['avg_duration'], datetime.timedelta(days=1, hours=12))

def test_sum_distinct_duration_field(self):
    vals = Publisher.objects.aggregate(total_duration=Sum('duration', distinct=True))
    self.assertEqual(vals['total_duration'], datetime.timedelta(days=3))

def test_annotate_then_aggregate_with_distinct(self):
    vals = Author.objects.annotate(book_count=Count('book')).aggregate(avg_distinct=Avg('book_count', distinct=True))
    self.assertEqual(vals['avg_distinct'], Approximate(1.5, places=3))

def test_get_repr_options_includes_distinct_flag(self):
    expr = Avg('rating', distinct=True)
    opts = expr._get_repr_options()
    self.assertIn('distinct', opts)
    self.assertTrue(opts['distinct'])

def test_avg_allows_distinct_and_sql_includes_distinct(self):
    with CaptureQueriesContext(connection) as captured:
        res = Book.objects.aggregate(avg=Avg('rating', distinct=True))
    self.assertEqual(res['avg'], 4.125)
    sql = captured[0]['sql'].upper()
    self.assertIn('DISTINCT', sql)

def test_sum_allows_distinct_and_sql_includes_distinct(self):
    with CaptureQueriesContext(connection) as captured:
        res = Book.objects.aggregate(s=Sum('rating', distinct=True))
    self.assertEqual(res['s'], 16.5)
    sql = captured[0]['sql'].upper()
    self.assertIn('DISTINCT', sql)

def test_sum_distinct_publisher_awards_value(self):
    res = Book.objects.aggregate(sum_distinct_awards=Sum('publisher__num_awards', distinct=True))
    self.assertEqual(res['sum_distinct_awards'], 20)

def test_sum_distinct_duration_field(self):
    res = Publisher.objects.aggregate(sum_duration=Sum('duration', distinct=True))
    self.assertEqual(res['sum_duration'], datetime.timedelta(days=3))

def test_get_repr_options_includes_distinct_for_avg(self):
    agg = Avg('rating', distinct=True)
    opts = agg._get_repr_options()
    self.assertIn('distinct', opts)
    self.assertTrue(opts['distinct'])

def test_get_repr_options_includes_distinct_for_sum(self):
    agg = Sum('rating', distinct=True)
    opts = agg._get_repr_options()
    self.assertIn('distinct', opts)
    self.assertTrue(opts['distinct'])

def test_avg_with_case_expression_and_distinct(self):
    case_expr = Case(When(pages__gt=300, then='rating'))
    with CaptureQueriesContext(connection) as captured:
        res = Book.objects.aggregate(avg_case=Avg(case_expr, distinct=True))
    self.assertEqual(res['avg_case'], 4.125)
    sql = captured[0]['sql'].upper()
    self.assertIn('DISTINCT', sql)

def test_sum_distinct_prices_per_publisher_annotation(self):
    qs = Publisher.objects.annotate(sum_distinct_prices=Sum('book__price', distinct=True))
    p1 = qs.get(pk=self.p1.pk)
    self.assertEqual(p1.sum_distinct_prices, Decimal('59.69'))
    self.assertIn('DISTINCT', str(qs.query).upper())

def test_avg_distinct_in_values_annotate_does_not_raise(self):
    vals = list(Book.objects.values('rating').annotate(avg_price_distinct=Avg('price', distinct=True)).order_by('rating'))
    self.assertTrue(len(vals) > 0)
    self.assertIn('avg_price_distinct', vals[0])

def test_sum_distinct_with_output_field_duration_works(self):
    res = Publisher.objects.aggregate(sum_duration_out=Sum('duration', distinct=True, output_field=DurationField()))
    self.assertEqual(res['sum_duration_out'], datetime.timedelta(days=3))

def test_avg_allows_distinct_flag_on_aggregate(self):
    vals = Book.objects.aggregate(avg=Avg('rating', distinct=True))
    self.assertEqual(vals['avg'], Approximate(4.125, places=3))

def test_sum_allows_distinct_flag_on_aggregate(self):
    vals = Book.objects.aggregate(total=Sum('rating', distinct=True))
    self.assertEqual(vals['total'], Approximate(16.5, places=3))

def test_avg_allows_distinct_on_publisher_books_annotate(self):
    publisher = Publisher.objects.annotate(avg_distinct=Avg('book__rating', distinct=True)).get(name='Apress')
    self.assertEqual(publisher.avg_distinct, Approximate(4.25, places=3))

def test_sum_allows_distinct_on_publisher_books_aggregate(self):
    vals = Publisher.objects.aggregate(sum_distinct=Sum('book__rating', distinct=True))
    self.assertEqual(vals['sum_distinct'], Approximate(16.5, places=3))

def test_as_sql_contains_distinct_for_avg(self):
    with CaptureQueriesContext(connection) as ctx:
        Book.objects.aggregate(avg=Avg('rating', distinct=True))
    sql = ctx.captured_queries[0]['sql'].upper()
    self.assertIn('DISTINCT', sql)

def test_as_sql_contains_distinct_for_sum(self):
    with CaptureQueriesContext(connection) as ctx:
        Book.objects.aggregate(total=Sum('rating', distinct=True))
    sql = ctx.captured_queries[0]['sql'].upper()
    self.assertIn('DISTINCT', sql)

def test_get_repr_options_includes_distinct(self):
    expr = Avg('rating', distinct=True)
    opts = expr._get_repr_options()
    self.assertIn('distinct', opts)
    self.assertTrue(opts['distinct'])

def test_sum_with_case_and_distinct(self):
    vals = Book.objects.aggregate(distinct_rating_sum=Sum(Case(When(pages__gt=300, then='rating')), distinct=True))
    self.assertEqual(vals['distinct_rating_sum'], Approximate(16.5, places=3))

def test_sum_distinct_on_duration_field(self):
    vals = Publisher.objects.aggregate(total_duration=Sum('duration', distinct=True, output_field=DurationField()))
    self.assertEqual(vals['total_duration'], datetime.timedelta(days=3))

def test_avg_allows_distinct_in_aggregate_and_sql(self):
    with CaptureQueriesContext(connection) as ctx:
        result = Book.objects.aggregate(Avg('rating', distinct=True))
    self.assertIn('rating__avg', result)
    self.assertEqual(result['rating__avg'], 4.125)
    sql = ctx.captured_queries[-1]['sql'].upper()
    self.assertIn('AVG(DISTINCT', sql)

def test_sum_allows_distinct_in_aggregate_and_sql(self):
    with CaptureQueriesContext(connection) as ctx:
        result = Book.objects.aggregate(Sum('rating', distinct=True))
    self.assertEqual(result['rating__sum'], 16.5)
    sql = ctx.captured_queries[-1]['sql'].upper()
    self.assertIn('SUM(DISTINCT', sql)

def test_count_allows_distinct_and_sql(self):
    with CaptureQueriesContext(connection) as ctx:
        result = Book.objects.aggregate(distinct_count=Count('rating', distinct=True))
    self.assertEqual(result['distinct_count'], 4)
    sql = ctx.captured_queries[-1]['sql'].upper()
    self.assertIn('COUNT(DISTINCT', sql)

def test_avg_and_sum_repr_options_and_copy_preserve_distinct(self):
    a = Avg('rating', distinct=True)
    self.assertTrue(a.distinct)
    opts = a._get_repr_options()
    self.assertIn('distinct', opts)
    self.assertTrue(opts['distinct'])
    b = a.copy()
    self.assertTrue(b.distinct)
    s = Sum('rating', distinct=True)
    self.assertTrue(s.distinct)
    s_opts = s._get_repr_options()
    self.assertIn('distinct', s_opts)
    self.assertTrue(s_opts['distinct'])
    s_copy = s.copy()
    self.assertTrue(s_copy.distinct)

def test_max_raises_on_distinct(self):
    msg = 'Max does not allow distinct.'
    with self.assertRaisesMessage(TypeError, msg):
        Max('rating', distinct=True)

def test_stddev_raises_on_distinct(self):
    msg = 'StdDev does not allow distinct.'
    with self.assertRaisesMessage(TypeError, msg):
        StdDev('rating', distinct=True)

def test_variance_raises_on_distinct(self):
    msg = 'Variance does not allow distinct.'
    with self.assertRaisesMessage(TypeError, msg):
        Variance('rating', distinct=True)

def test_sum_distinct_matches_manual_distinct_sum(self):
    agg = Book.objects.aggregate(sum_distinct=Sum('rating', distinct=True))
    self.assertEqual(agg['sum_distinct'], 16.5)
    distinct_ratings = list(Book.objects.values_list('rating', flat=True).distinct())
    self.assertAlmostEqual(sum(distinct_ratings), 16.5, places=6)

def test_aggregate_default_alias_with_distinct(self):
    result = Book.objects.aggregate(Avg('rating', distinct=True))
    self.assertIn('rating__avg', result)

def test_constructing_avg_and_sum_with_distinct_does_not_raise(self):
    try:
        Avg('rating', distinct=True)
        Sum('rating', distinct=True)
    except Exception as e:
        self.fail('Constructing Avg/Sum with distinct=True raised %r' % e)

from django.db.models import Q
from decimal import Decimal
import datetime
from django.db.models import Avg, Sum, Max
from django.test.utils import Approximate
from .tests import aggregation as _agg_module

def test_avg_allows_distinct_in_aggregate(self):
    res = Book.objects.aggregate(avg_distinct=Avg('rating', distinct=True))
    self.assertEqual(res['avg_distinct'], 4.125)
AggregateTestCase.test_avg_allows_distinct_in_aggregate = test_avg_allows_distinct_in_aggregate

def test_sum_allows_distinct_decimal(self):
    res = Book.objects.aggregate(sum_price_distinct=Sum('price', distinct=True))
    self.assertEqual(res['sum_price_distinct'], Decimal('240.58'))
AggregateTestCase.test_sum_allows_distinct_decimal = test_sum_allows_distinct_decimal

def test_sum_allows_distinct_on_duration(self):
    res = Publisher.objects.aggregate(sum_duration_distinct=Sum('duration', distinct=True))
    self.assertEqual(res['sum_duration_distinct'], datetime.timedelta(days=3))
AggregateTestCase.test_sum_allows_distinct_on_duration = test_sum_allows_distinct_on_duration

def test_avg_allows_distinct_in_annotate(self):
    p = Publisher.objects.annotate(avg_price=Avg('book__price', distinct=True)).get(name='Prentice Hall')
    self.assertEqual(p.avg_price, Approximate(Decimal('56.245'), places=3))
AggregateTestCase.test_avg_allows_distinct_in_annotate = test_avg_allows_distinct_in_annotate

def test_sum_allows_distinct_in_annotate(self):
    p = Publisher.objects.annotate(sum_price=Sum('book__price', distinct=True)).get(name='Apress')
    self.assertEqual(p.sum_price, Decimal('59.69'))
AggregateTestCase.test_sum_allows_distinct_in_annotate = test_sum_allows_distinct_in_annotate

def test_max_rejects_distinct(self):
    with self.assertRaisesMessage(TypeError, 'Max does not allow distinct.'):
        Max('pages', distinct=True)
AggregateTestCase.test_max_rejects_distinct = test_max_rejects_distinct

def test_avg_default_alias_unchanged_with_distinct(self):
    self.assertEqual(Avg('rating', distinct=True).default_alias, 'rating__avg')
AggregateTestCase.test_avg_default_alias_unchanged_with_distinct = test_avg_default_alias_unchanged_with_distinct

def test_sum_distinct_on_ratings_aggregate(self):
    res = Book.objects.aggregate(sum_rating_distinct=Sum('rating', distinct=True))
    self.assertEqual(res['sum_rating_distinct'], 16.5)
AggregateTestCase.test_sum_distinct_on_ratings_aggregate = test_sum_distinct_on_ratings_aggregate

def test_get_repr_options_includes_distinct(self):
    self.assertTrue(Avg('rating', distinct=True)._get_repr_options().get('distinct'))
    self.assertTrue(Sum('price', distinct=True)._get_repr_options().get('distinct'))
AggregateTestCase.test_get_repr_options_includes_distinct = test_get_repr_options_includes_distinct

def test_sum_distinct_with_filter(self):
    from django.db.models import Q
    res = Book.objects.aggregate(sum_distinct_filtered=Sum('price', distinct=True, filter=Q(rating__gte=4.0)))
    self.assertEqual(res['sum_distinct_filtered'], Decimal('217.49'))
AggregateTestCase.test_sum_distinct_with_filter = test_sum_distinct_with_filter