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