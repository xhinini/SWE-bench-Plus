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

def test_avg_class_allows_distinct_flag(self):
    self.assertTrue(Avg.allow_distinct)

def test_sum_class_allows_distinct_flag(self):
    self.assertTrue(Sum.allow_distinct)

def test_avg_instantiation_with_distinct_does_not_raise_and_has_option(self):
    expr = Avg('rating', distinct=True)
    self.assertTrue(expr.distinct)
    opts = expr._get_repr_options()
    self.assertIn('distinct', opts)
    self.assertTrue(opts['distinct'])

def test_sum_instantiation_with_distinct_does_not_raise_and_has_option(self):
    expr = Sum('pages', distinct=True)
    self.assertTrue(expr.distinct)
    opts = expr._get_repr_options()
    self.assertIn('distinct', opts)
    self.assertTrue(opts['distinct'])

def test_aggregate_query_with_avg_distinct_runs_and_returns_expected_value(self):
    res = Book.objects.aggregate(avg_rating=Avg('rating', distinct=True))
    self.assertIn('avg_rating', res)
    self.assertEqual(res['avg_rating'], 4.125)

def test_aggregate_query_with_sum_distinct_runs_and_returns_expected_value(self):
    res = Book.objects.aggregate(sum_ratings=Sum('rating', distinct=True))
    self.assertIn('sum_ratings', res)
    self.assertEqual(res['sum_ratings'], 16.5)

def test_avg_distinct_appears_in_executed_sql(self):
    with CaptureQueriesContext(connection) as ctx:
        Book.objects.aggregate(avg_rating=Avg('rating', distinct=True))
    self.assertTrue(len(ctx.captured_queries) >= 1)
    sql = ctx.captured_queries[0]['sql'].upper()
    self.assertIn('DISTINCT', sql)

def test_sum_distinct_appears_in_executed_sql(self):
    with CaptureQueriesContext(connection) as ctx:
        Book.objects.aggregate(sum_rating=Sum('rating', distinct=True))
    self.assertTrue(len(ctx.captured_queries) >= 1)
    sql = ctx.captured_queries[0]['sql'].upper()
    self.assertIn('DISTINCT', sql)

def test_annotate_with_avg_distinct_per_row(self):
    b = Book.objects.filter(pk=self.b1.pk).annotate(distinct_authors_age=Avg('authors__age', distinct=True)).get()
    self.assertEqual(b.distinct_authors_age, 34.5)

def test_annotate_with_sum_distinct_per_row(self):
    b = Book.objects.filter(pk=self.b4.pk).annotate(distinct_authors_age_sum=Sum('authors__age', distinct=True)).get()
    self.assertEqual(b.distinct_authors_age_sum, 37 + 29 + 25)

from django.db.models import Q, DecimalField

def test_avg_allows_distinct_in_aggregate(self):
    vals = Book.objects.aggregate(ratings=Avg('rating', distinct=True))
    self.assertEqual(vals['ratings'], Approximate(4.125, places=3))

def test_sum_allows_distinct_in_aggregate(self):
    vals = Book.objects.aggregate(ratings=Sum('rating', distinct=True))
    self.assertEqual(vals['ratings'], 16.5)

def test_avg_distinct_in_annotation(self):
    qs = Book.objects.annotate(avg_unique_authors_age=Avg('authors__age', distinct=True))
    b1 = qs.get(pk=self.b1.pk)
    self.assertEqual(b1.avg_unique_authors_age, 34.5)

def test_sum_distinct_with_output_field_decimal(self):
    vals = Book.objects.aggregate(total=Sum('price', distinct=True, output_field=DecimalField()))
    self.assertEqual(vals['total'], Decimal('240.58'))

def test_avg_distinct_with_case_expression(self):
    case_expr = Case(When(pages__gt=400, then='rating'))
    vals = Book.objects.aggregate(avg=Avg(case_expr, distinct=True))
    self.assertEqual(vals['avg'], 4.0)

def test_sum_distinct_values_groupby(self):
    qs = Book.objects.values('rating').annotate(sum_pages_distinct=Sum('pages', distinct=True)).order_by('rating')
    results = list(qs)
    self.assertTrue(len(results) >= 1)
    self.assertIsNotNone(results[0]['sum_pages_distinct'])

def test_avg_distinct_with_filter_kwarg(self):
    vals = Book.objects.aggregate(avg=Avg('rating', distinct=True, filter=Q(rating__gt=3)))
    self.assertEqual(vals['avg'], 4.5)

def test_sum_distinct_over_m2m(self):
    vals = Book.objects.aggregate(sum_authors_ages_distinct=Sum('authors__age', distinct=True))
    self.assertEqual(vals['sum_authors_ages_distinct'], 308)

def test_avg_distinct_get_repr_options_includes_distinct(self):
    expr = Avg('rating', distinct=True)
    opts = expr._get_repr_options()
    self.assertIn('distinct', opts)
    self.assertTrue(opts['distinct'])

def test_distinct_appears_in_generated_sql_for_aggregates(self):
    with CaptureQueriesContext(connection) as ctx:
        Book.objects.aggregate(r=Avg('rating', distinct=True))
    sql = ctx.captured_queries[0]['sql']
    self.assertIn('DISTINCT', sql.upper())

def test_avg_allows_distinct_aggregate(self):
    vals = Book.objects.aggregate(Avg('rating', distinct=True))
    self.assertEqual(vals, {'rating__avg': Approximate(4.125, places=3)})

def test_sum_allows_distinct_aggregate(self):
    vals = Book.objects.aggregate(Sum('rating', distinct=True))
    self.assertEqual(vals, {'rating__sum': Approximate(16.5, places=2)})

def test_publisher_sum_distinct_book_prices(self):
    vals = Publisher.objects.aggregate(total=Sum('book__price', distinct=True))
    self.assertEqual(vals['total'], Decimal('240.58'))

def test_custom_aggregate_disallowing_distinct_raises(self):

    class NoDistinct(Aggregate):
        function = 'MYAGG'
        name = 'NoDistinct'
    with self.assertRaisesMessage(TypeError, 'NoDistinct does not allow distinct.'):
        NoDistinct('rating', distinct=True)

def test_count_star_with_filter_raises_valueerror(self):
    with self.assertRaisesMessage(ValueError, 'Star cannot be used with filter. Please specify a field.'):
        Count('*', filter=Value(True))

def test_get_source_expressions_includes_filter_at_end(self):
    ag = Avg('rating', filter=Value(True))
    exprs = ag.get_source_expressions()
    self.assertIs(exprs[-1], ag.filter)
    self.assertEqual(len(ag.get_source_fields()), 1)

def test_repr_options_include_distinct_for_avg(self):
    ag = Avg('rating', distinct=True)
    opts = ag._get_repr_options()
    self.assertIn('distinct', opts)
    self.assertTrue(opts['distinct'])

def test_repr_options_include_distinct_for_sum(self):
    ag = Sum('rating', distinct=True)
    opts = ag._get_repr_options()
    self.assertIn('distinct', opts)
    self.assertTrue(opts['distinct'])

def test_aggregate_default_alias_with_distinct_for_avg(self):
    vals = Book.objects.aggregate(Avg('rating', distinct=True))
    self.assertEqual(list(vals.keys()), ['rating__avg'])

def test_get_source_fields_excludes_filter(self):
    ag = Sum('rating', filter=Value(True))
    source_fields = ag.get_source_fields()
    self.assertEqual(len(source_fields), 1)

def test_avg_allows_distinct_aggregate_result(self):
    vals = Book.objects.aggregate(avg=Avg('rating', distinct=True))
    self.assertEqual(vals, {'avg': Approximate(4.125, places=3)})

def test_sum_allows_distinct_aggregate_result(self):
    vals = Book.objects.aggregate(sum=Sum('rating', distinct=True))
    self.assertEqual(vals, {'sum': 16.5})

def test_avg_distinct_with_alias_kwarg(self):
    vals = Book.objects.aggregate(distinct_avg=Avg('rating', distinct=True))
    self.assertIn('distinct_avg', vals)
    self.assertEqual(vals['distinct_avg'], Approximate(4.125, places=3))

def test_sum_distinct_with_alias_kwarg(self):
    vals = Book.objects.aggregate(distinct_sum=Sum('rating', distinct=True))
    self.assertIn('distinct_sum', vals)
    self.assertEqual(vals['distinct_sum'], 16.5)

def test_max_rejects_distinct(self):
    with self.assertRaisesMessage(TypeError, 'Max does not allow distinct.'):
        Max('rating', distinct=True)

def test_distinct_in_sql_for_avg(self):
    with CaptureQueriesContext(connection) as ctx:
        Book.objects.aggregate(avg=Avg('rating', distinct=True))
    self.assertTrue(ctx.captured_queries)
    sql = ctx.captured_queries[0]['sql'].lower()
    self.assertIn('distinct', sql)

def test_average_distinct_with_case_expression(self):
    agg = Book.objects.aggregate(avg=Avg(Case(When(pages__gt=300, then='rating')), distinct=True))
    self.assertEqual(agg['avg'], Approximate(4.125, places=3))

def test_sum_distinct_with_case_expression(self):
    agg = Book.objects.aggregate(sum=Sum(Case(When(pages__gt=300, then='rating')), distinct=True))
    self.assertEqual(agg['sum'], 16.5)

def test_repr_includes_distinct_for_avg(self):
    expr = Avg('rating', distinct=True)
    r = repr(expr)
    self.assertIn('distinct=True', r)

def test_min_rejects_distinct_error_message(self):
    with self.assertRaisesMessage(TypeError, 'Min does not allow distinct.'):
        Min('rating', distinct=True)

def test_regression_avg_allows_distinct_aggregate(self):
    vals = Book.objects.aggregate(avg_distinct=Avg('rating', distinct=True))
    self.assertEqual(vals['avg_distinct'], 4.125)

def test_regression_sum_allows_distinct_duration_aggregate(self):
    vals = Publisher.objects.aggregate(duration_sum_distinct=Sum('duration', distinct=True))
    self.assertEqual(vals['duration_sum_distinct'], datetime.timedelta(days=3))

def test_regression_avg_allows_distinct_annotate(self):
    qs = Book.objects.annotate(avg_distinct_rating=Avg('rating', distinct=True)).order_by('pk')
    b = qs.get(pk=self.b1.pk)
    self.assertTrue(hasattr(b, 'avg_distinct_rating'))
    self.assertEqual(b.avg_distinct_rating, 4.5)

def test_regression_sum_allows_distinct_annotate_numeric(self):
    qs = Publisher.objects.annotate(distinct_book_price_sum=Sum('book__price', distinct=True)).order_by('pk')
    p1 = qs.get(pk=self.p1.pk)
    self.assertEqual(p1.distinct_book_price_sum, Decimal('59.69'))

def test_regression_avg_distinct_generates_distinct_in_sql(self):
    with CaptureQueriesContext(connection) as captured:
        Book.objects.aggregate(avg_distinct=Avg('rating', distinct=True))
    sql = captured.captured_queries[-1]['sql'].upper()
    self.assertIn('DISTINCT', sql)

def test_regression_sum_distinct_generates_distinct_in_sql(self):
    with CaptureQueriesContext(connection) as captured:
        Book.objects.aggregate(sum_distinct=Sum('rating', distinct=True))
    sql = captured.captured_queries[-1]['sql'].upper()
    self.assertIn('DISTINCT', sql)

def test_regression_repr_includes_distinct_option(self):
    expr = Avg('rating', distinct=True)
    self.assertIn('distinct', repr(expr))

def test_regression_default_alias_with_distinct(self):
    expr = Avg(Value(1, output_field=IntegerField()), distinct=True)
    with self.assertRaises(TypeError):
        _ = expr.default_alias
    expr2 = Avg(F('rating'), distinct=True)
    self.assertTrue(expr2.default_alias.endswith('__avg'))
    self.assertIn('rating', expr2.default_alias)

def test_regression_sum_distinct_on_duration_annotate(self):
    qs = Publisher.objects.annotate(duration_distinct_sum=Sum('duration', distinct=True)).order_by('pk')
    p1 = qs.get(pk=self.p1.pk)
    self.assertEqual(p1.duration_distinct_sum, datetime.timedelta(days=1))

def test_regression_avg_distinct_with_values_and_aggregate(self):
    vals = Book.objects.values('rating').aggregate(avg_distinct=Avg('rating', distinct=True))
    self.assertEqual(vals['avg_distinct'], 4.125)

def test_regression_avg_allows_distinct_in_aggregate(self):
    vals = Book.objects.aggregate(ratings=Avg('rating', distinct=True))
    self.assertEqual(vals['ratings'], Approximate(4.125, places=3))

def test_regression_sum_allows_distinct_in_aggregate(self):
    vals = Book.objects.aggregate(ratings=Sum('rating', distinct=True))
    self.assertEqual(vals['ratings'], 16.5)

def test_regression_avg_allows_distinct_in_annotate(self):
    b = Book.objects.annotate(distinct_author_age=Avg('authors__age', distinct=True)).get(pk=self.b1.pk)
    self.assertEqual(b.distinct_author_age, 34.5)

def test_regression_sum_allows_distinct_in_annotate_reverse_fk(self):
    pubs = list(Publisher.objects.annotate(price_sum=Sum('book__price', distinct=True)).order_by('name').values_list('name', 'price_sum'))
    expected = [('Apress', Decimal('59.69')), ("Jonno's House of Books", None), ('Morgan Kaufmann', Decimal('75.00')), ('Prentice Hall', Decimal('112.49')), ('Sams', Decimal('23.09'))]
    self.assertEqual(pubs, expected)

def test_regression_avg_construction_does_not_raise(self):
    agg = Avg('rating', distinct=True)
    self.assertIsInstance(agg, Avg)

def test_regression_sum_construction_does_not_raise(self):
    agg = Sum('rating', distinct=True)
    self.assertIsInstance(agg, Sum)

def test_regression_avg_used_in_expression(self):
    vals = Book.objects.aggregate(avg_plus_one=Avg('rating', distinct=True) + 1)
    self.assertEqual(vals['avg_plus_one'], Approximate(5.125, places=3))

def test_regression_sum_used_in_expression(self):
    vals = Book.objects.aggregate(sum_times_two=Sum('rating', distinct=True) * 2)
    self.assertEqual(vals['sum_times_two'], 33.0)

def test_regression_default_alias_with_distinct(self):
    alias = Avg('rating', distinct=True).default_alias
    self.assertEqual(alias, 'rating__avg')

def test_regression_sum_distinct_duration_field(self):
    vals = Publisher.objects.aggregate(duration_sum_distinct=Sum('duration', distinct=True))
    self.assertEqual(vals['duration_sum_distinct'], datetime.timedelta(days=3))

from django.db.models import Q

def test_sum_allows_distinct_in_aggregate_basic(self):
    vals = Book.objects.aggregate(ratings=Sum('rating', distinct=True))
    self.assertEqual(vals['ratings'], 16.5)

def test_sum_allows_distinct_with_decimal_field(self):
    vals = Book.objects.aggregate(total_price=Sum('price', distinct=True))
    self.assertEqual(vals['total_price'], Decimal('240.58'))

def test_sum_allows_distinct_in_annotate(self):
    publisher = Publisher.objects.annotate(sum_price=Sum('book__price', distinct=True)).get(name='Apress')
    self.assertEqual(publisher.sum_price, Decimal('59.69'))

def test_sum_distinct_generates_distinct_in_sql(self):
    with CaptureQueriesContext(connection) as ctx:
        Book.objects.aggregate(total=Sum('rating', distinct=True))
    sql = ctx.captured_queries[-1]['sql'].upper()
    self.assertIn('DISTINCT', sql)
    self.assertIn('SUM', sql)

def test_sum_get_repr_options_includes_distinct(self):
    s = Sum('rating', distinct=True)
    opts = s._get_repr_options()
    self.assertIn('distinct', opts)
    self.assertTrue(opts['distinct'])

def test_sum_with_f_expression_and_distinct(self):
    vals = Book.objects.aggregate(pages_sum=Sum(F('pages'), distinct=True))
    self.assertEqual(vals['pages_sum'], 3703)

def test_sum_distinct_with_filter_expression(self):
    from django.db.models import Q
    vals = Book.objects.aggregate(high_ratings=Sum('rating', distinct=True, filter=Q(rating__gt=4)))
    self.assertEqual(vals['high_ratings'], 5.0)

def test_sum_constructor_allows_distinct(self):
    s = Sum('rating', distinct=True)
    self.assertIsInstance(s, Sum)

def test_sum_distinct_in_values_annotate_grouping(self):
    qs = Book.objects.values('rating').annotate(pages_sum=Sum('pages', distinct=True))
    entry = qs.get(rating=4.5)
    self.assertEqual(entry['pages_sum'], 447)

from unittest.mock import patch
from django.db.models import Q

def test_avg_distinct_aggregate_value_and_sql_contains_distinct(self):
    with CaptureQueriesContext(connection) as ctx:
        res = Book.objects.aggregate(avg=Avg('rating', distinct=True))
    self.assertTrue(ctx.captured_queries)
    sql = ctx.captured_queries[-1]['sql'].upper()
    self.assertIn('DISTINCT', sql)
    self.assertEqual(res['avg'], 4.125)

def test_sum_distinct_aggregate_value_and_sql_contains_distinct(self):
    with CaptureQueriesContext(connection) as ctx:
        res = Book.objects.aggregate(s=Sum('rating', distinct=True))
    self.assertTrue(ctx.captured_queries)
    sql = ctx.captured_queries[-1]['sql'].upper()
    self.assertIn('DISTINCT', sql)
    self.assertEqual(res['s'], 16.5)

def test_avg_distinct_annotation_query_contains_distinct(self):
    qs = Book.objects.annotate(avg_rating=Avg('rating', distinct=True)).order_by('pk')
    sql = str(qs.query).upper()
    self.assertIn('DISTINCT', sql)

def test_sum_distinct_annotation_query_contains_distinct(self):
    qs = Book.objects.annotate(sum_pages=Sum('pages', distinct=True)).order_by('pk')
    sql = str(qs.query).upper()
    self.assertIn('DISTINCT', sql)

def test_repr_options_contains_distinct_for_avg_and_sum(self):
    a = Avg('age', distinct=True)
    s = Sum('price', distinct=True)
    self.assertIn('distinct', a._get_repr_options())
    self.assertTrue(a._get_repr_options()['distinct'])
    self.assertIn('distinct', s._get_repr_options())
    self.assertTrue(s._get_repr_options()['distinct'])

def test_count_star_with_filter_raises_value_error(self):
    from django.db.models import Q
    with self.assertRaises(ValueError):
        Count('*', filter=Q(pk__isnull=False))

def test_aggregate_filter_clause_used_when_supported(self):
    from django.db.models import Q
    with patch.object(connection.features, 'supports_aggregate_filter_clause', True):
        with CaptureQueriesContext(connection) as ctx:
            res = Author.objects.aggregate(avg_over_30=Avg('age', distinct=True, filter=Q(age__gt=30)))
        self.assertTrue(ctx.captured_queries)
        sql = ctx.captured_queries[-1]['sql'].upper()
        self.assertIn('FILTER (WHERE', sql)

def test_aggregate_filter_clause_not_used_when_unsupported(self):
    from django.db.models import Q
    with patch.object(connection.features, 'supports_aggregate_filter_clause', False):
        with CaptureQueriesContext(connection) as ctx:
            res = Author.objects.aggregate(avg_over_30=Avg('age', distinct=True, filter=Q(age__gt=30)))
        self.assertTrue(ctx.captured_queries)
        sql = ctx.captured_queries[-1]['sql'].upper()
        self.assertNotIn('FILTER (WHERE', sql)
        self.assertTrue('CASE' in sql or 'WHEN' in sql)

def test_sum_distinct_in_values_annotation_runs(self):
    qs = Book.objects.values('rating').annotate(sum_distinct_pages=Sum('pages', distinct=True)).order_by('rating')
    rows = list(qs)
    self.assertIsInstance(rows, list)
    self.assertGreaterEqual(len(rows), 1)

def test_avg_and_sum_distinct_aggregate_on_price(self):
    from decimal import Decimal
    res = Book.objects.aggregate(avg_price_distinct=Avg('price', distinct=True), sum_price_distinct=Sum('price', distinct=True))
    self.assertEqual(res['sum_price_distinct'], Decimal('240.58'))
    self.assertEqual(res['avg_price_distinct'], Approximate(Decimal('48.116'), places=2))