from unittest.mock import patch

def test_count_distinct_sql_contains_space(self):
    """Aggregate COUNT(distinct=...) should render 'COUNT(DISTINCT ' (note the trailing space)."""
    with CaptureQueriesContext(connection) as ctx:
        Book.objects.aggregate(n=Count('rating', distinct=True))
    sql = ctx.captured_queries[0]['sql']
    self.assertIn('COUNT(DISTINCT ', sql)

def test_annotate_count_distinct_sql_contains_space(self):
    """Annotated COUNT(distinct=...) should render 'COUNT(DISTINCT ' in the SELECT."""
    qs = Book.objects.annotate(n=Count('rating', distinct=True)).order_by('pk')
    with CaptureQueriesContext(connection) as ctx:
        list(qs[:1])
    sql = ctx.captured_queries[0]['sql']
    self.assertIn('COUNT(DISTINCT ', sql)

def test_count_distinct_on_related_field_sql_contains_space(self):
    """COUNT(distinct=...) on a related field should also render 'COUNT(DISTINCT '."""
    with CaptureQueriesContext(connection) as ctx:
        Book.objects.aggregate(distinct_authors=Count('authors__id', distinct=True))
    sql = ctx.captured_queries[0]['sql']
    self.assertIn('COUNT(DISTINCT ', sql)

def test_count_distinct_with_case_expression_sql_contains_space(self):
    """COUNT(distinct=...) with a Case/When expression should render 'COUNT(DISTINCT '."""
    expr = Case(When(pages__gt=300, then='rating'))
    with CaptureQueriesContext(connection) as ctx:
        Book.objects.aggregate(distinct_ratings=Count(expr, distinct=True))
    sql = ctx.captured_queries[0]['sql']
    self.assertIn('COUNT(DISTINCT ', sql)

def test_multiple_aggregates_one_distinct_and_one_non_distinct(self):
    """A query with both distinct and non-distinct COUNT() should render DISTINCT with the trailing space and also include a plain COUNT."""
    with CaptureQueriesContext(connection) as ctx:
        Book.objects.aggregate(d=Count('rating', distinct=True), nd=Count('rating'))
    sql = ctx.captured_queries[0]['sql']
    self.assertIn('COUNT(DISTINCT ', sql)
    self.assertIn('COUNT(', sql)

def test_count_without_distinct_does_not_include_distinct(self):
    """COUNT without distinct must not include a DISTINCT token."""
    with CaptureQueriesContext(connection) as ctx:
        Book.objects.aggregate(n=Count('rating'))
    sql = ctx.captured_queries[0]['sql']
    self.assertNotIn('COUNT(DISTINCT ', sql)

def test_values_annotate_count_distinct_sql_contains_space(self):
    """values(...).annotate(Count(..., distinct=True)) should include 'COUNT(DISTINCT ' in the generated SQL."""
    qs = Book.objects.values('rating').annotate(n=Count('id', distinct=True)).order_by('rating')
    with CaptureQueriesContext(connection) as ctx:
        list(qs)
    sql = ctx.captured_queries[0]['sql']
    self.assertIn('COUNT(DISTINCT ', sql)

def test_aggregate_with_filter_backend_supports_filter_clause_includes_distinct_and_filter(self):
    """When the backend supports FILTER (WHERE ...), we should see the FILTER clause and 'DISTINCT ' with trailing space."""
    with patch.object(connection.features, 'supports_aggregate_filter_clause', True):
        with CaptureQueriesContext(connection) as ctx:
            Book.objects.aggregate(n=Count('rating', distinct=True, filter=Value(True)))
        sql = ctx.captured_queries[0]['sql']
    self.assertIn('FILTER (WHERE', sql.upper())
    self.assertIn('COUNT(DISTINCT ', sql)

def test_aggregate_with_filter_backend_without_filter_clause_uses_case_and_includes_distinct(self):
    """When the backend does not support FILTER (WHERE ...), the code uses CASE/WHEN to emulate filtering and must still include 'DISTINCT '."""
    with patch.object(connection.features, 'supports_aggregate_filter_clause', False):
        with CaptureQueriesContext(connection) as ctx:
            Book.objects.aggregate(n=Count('rating', distinct=True, filter=Value(True)))
        sql = ctx.captured_queries[0]['sql']
    self.assertNotIn('FILTER (WHERE'.upper(), sql.upper())
    self.assertIn('CASE', sql.upper())
    self.assertIn('COUNT(DISTINCT ', sql)

def test__get_repr_options_includes_distinct_and_filter_keys(self):
    """Ensure _get_repr_options exposes 'distinct' and 'filter' keys for Count(..., distinct=True, filter=...)."""
    c = Count('rating', distinct=True, filter=Value(True))
    opts = c._get_repr_options()
    self.assertIn('distinct', opts)
    self.assertTrue(opts['distinct'])
    self.assertIn('filter', opts)