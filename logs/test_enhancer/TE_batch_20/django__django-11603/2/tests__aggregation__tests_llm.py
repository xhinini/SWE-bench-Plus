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