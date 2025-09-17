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

def test_aggregate_count_distinct_has_space(self):
    from django.db import connection
    from django.db.models import Count
    from django.test.utils import CaptureQueriesContext
    with CaptureQueriesContext(connection) as ctx:
        Book.objects.aggregate(n=Count('rating', distinct=True))
    sql = ctx.captured_queries[0]['sql'].lower()
    self.assertIn('count(distinct ', sql)

def test_annotate_count_distinct_str_query_has_space(self):
    from django.db.models import Count
    qs = Book.objects.annotate(n=Count('rating', distinct=True))
    sql = str(qs.query).lower()
    self.assertIn('count(distinct ', sql)

def test_aggregate_count_distinct_on_related_field_has_space(self):
    from django.db import connection
    from django.db.models import Count
    from django.test.utils import CaptureQueriesContext
    with CaptureQueriesContext(connection) as ctx:
        Publisher.objects.aggregate(n=Count('book__id', distinct=True))
    sql = ctx.captured_queries[0]['sql'].lower()
    self.assertIn('count(distinct ', sql)

def test_annotate_count_distinct_on_related_field_str_query_has_space(self):
    from django.db.models import Count
    qs = Publisher.objects.annotate(n=Count('book__id', distinct=True))
    sql = str(qs.query).lower()
    self.assertIn('count(distinct ', sql)

def test_aggregate_count_distinct_with_case_expression_has_space(self):
    from django.db import connection
    from django.db.models import Count, Case, When
    from django.test.utils import CaptureQueriesContext
    case_expr = Case(When(pages__gt=300, then='rating'))
    with CaptureQueriesContext(connection) as ctx:
        Book.objects.aggregate(n=Count(case_expr, distinct=True))
    sql = ctx.captured_queries[0]['sql'].lower()
    self.assertIn('count(distinct ', sql)

def test_annotate_count_distinct_with_case_expression_str_query_has_space(self):
    from django.db.models import Count, Case, When
    case_expr = Case(When(pages__gt=300, then='rating'))
    qs = Book.objects.annotate(n=Count(case_expr, distinct=True))
    sql = str(qs.query).lower()
    self.assertIn('count(distinct ', sql)

def test_aggregate_count_distinct_with_f_expression_has_space(self):
    from django.db import connection
    from django.db.models import Count, F
    from django.test.utils import CaptureQueriesContext
    with CaptureQueriesContext(connection) as ctx:
        Book.objects.aggregate(n=Count(F('rating'), distinct=True))
    sql = ctx.captured_queries[0]['sql'].lower()
    self.assertIn('count(distinct ', sql)

def test_annotate_count_distinct_with_f_expression_str_query_has_space(self):
    from django.db.models import Count, F
    qs = Book.objects.annotate(n=Count(F('rating'), distinct=True))
    sql = str(qs.query).lower()
    self.assertIn('count(distinct ', sql)

def test_values_annotate_count_distinct_in_grouping_has_space(self):
    from django.db.models import Count
    qs = Book.objects.values('rating').annotate(n=Count('id', distinct=True))
    sql = str(qs.query).lower()
    self.assertIn('count(distinct ', sql)

def test_aggregate_count_distinct_authors_alias_has_space(self):
    from django.db import connection
    from django.db.models import Count
    from django.test.utils import CaptureQueriesContext
    with CaptureQueriesContext(connection) as ctx:
        Book.objects.aggregate(distinct_authors=Count('authors__id', distinct=True))
    sql = ctx.captured_queries[0]['sql'].lower()
    self.assertIn('count(distinct ', sql)

from django.test.utils import CaptureQueriesContext
from django.db import connection
from django.db.models import Count, Avg, Max
from django.db.models.expressions import Case, When

def test_aggregate_count_distinct_sql(self):
    """Aggregate() with Count(..., distinct=True) should render 'COUNT(DISTINCT ' in SQL."""
    with CaptureQueriesContext(connection) as captured:
        Book.objects.aggregate(n=Count('rating', distinct=True))
    sqls = [q['sql'].lower() for q in captured.captured_queries]
    self.assertTrue(any(('count(distinct ' in s for s in sqls)), msg='COUNT(DISTINCT <space> missing in aggregate SQL: %s' % sqls)

def test_annotate_count_distinct_sql(self):
    """annotate() with Count(..., distinct=True) should render 'COUNT(DISTINCT ' in SQL."""
    qs = Book.objects.annotate(n=Count('rating', distinct=True)).order_by('pk')
    with CaptureQueriesContext(connection) as captured:
        list(qs)
    sqls = [q['sql'].lower() for q in captured.captured_queries]
    self.assertTrue(any(('count(distinct ' in s for s in sqls)), msg='COUNT(DISTINCT <space> missing in annotate SQL: %s' % sqls)

def test_values_aggregate_count_distinct_sql(self):
    """values(...).aggregate(Count(..., distinct=True)) should render 'COUNT(DISTINCT ' in SQL."""
    with CaptureQueriesContext(connection) as captured:
        Book.objects.values('rating').aggregate(distinct_count=Count('rating', distinct=True))
    sqls = [q['sql'].lower() for q in captured.captured_queries]
    self.assertTrue(any(('count(distinct ' in s for s in sqls)), msg='COUNT(DISTINCT <space> missing in values().aggregate SQL: %s' % sqls)

def test_count_distinct_case_expression_sql(self):
    """COUNT(Case(...), distinct=True) should render 'COUNT(DISTINCT ' in SQL."""
    case_expr = Case(When(pages__gt=300, then='rating'))
    with CaptureQueriesContext(connection) as captured:
        Book.objects.aggregate(distinct_ratings=Count(case_expr, distinct=True))
    sqls = [q['sql'].lower() for q in captured.captured_queries]
    self.assertTrue(any(('count(distinct ' in s for s in sqls)), msg='COUNT(DISTINCT <space> missing in COUNT(Case(...)) SQL: %s' % sqls)

def test_count_star_distinct_sql(self):
    """COUNT('*', distinct=True) should render 'COUNT(DISTINCT ' in SQL (if the backend shows '*')."""
    with CaptureQueriesContext(connection) as captured:
        Book.objects.aggregate(n=Count('*', distinct=True))
    sqls = [q['sql'].lower() for q in captured.captured_queries]
    self.assertTrue(any(('count(distinct ' in s for s in sqls)), msg="COUNT(DISTINCT <space> missing in COUNT('*') SQL: %s" % sqls)

def test_annotate_values_list_count_distinct_sql(self):
    """values(...).annotate(Count(..., distinct=True)) should render 'COUNT(DISTINCT ' in SQL."""
    qs = Book.objects.values('rating').annotate(n=Count('authors__id', distinct=True)).order_by('rating')
    with CaptureQueriesContext(connection) as captured:
        list(qs)
    sqls = [q['sql'].lower() for q in captured.captured_queries]
    self.assertTrue(any(('count(distinct ' in s for s in sqls)), msg='COUNT(DISTINCT <space> missing in values().annotate SQL: %s' % sqls)

def test_grouped_annotation_count_distinct_sql(self):
    """Annotating related fields with distinct=True should render 'COUNT(DISTINCT ' in SQL."""
    qs = Publisher.objects.annotate(dnum=Count('book__id', distinct=True)).order_by('pk')
    with CaptureQueriesContext(connection) as captured:
        list(qs)
    sqls = [q['sql'].lower() for q in captured.captured_queries]
    self.assertTrue(any(('count(distinct ' in s for s in sqls)), msg='COUNT(DISTINCT <space> missing in grouped annotation SQL: %s' % sqls)

def test_distinct_in_annotation_on_related(self):
    """Count distinct on a reverse FK in annotate() should render 'COUNT(DISTINCT ' in SQL."""
    qs = Author.objects.annotate(num_books_distinct=Count('book__isbn', distinct=True)).order_by('pk')
    with CaptureQueriesContext(connection) as captured:
        list(qs)
    sqls = [q['sql'].lower() for q in captured.captured_queries]
    self.assertTrue(any(('count(distinct ' in s for s in sqls)), msg='COUNT(DISTINCT <space> missing in reverse FK annotate SQL: %s' % sqls)

def test_count_distinct_in_subquery_aggregate_sql(self):
    """Annotate with distinct and then aggregate over that annotation should include 'COUNT(DISTINCT ' in SQL."""
    qs = Book.objects.annotate(n_authors=Count('authors', distinct=True))
    with CaptureQueriesContext(connection) as captured:
        qs.aggregate(max_n=Max('n_authors'))
    sqls = [q['sql'].lower() for q in captured.captured_queries]
    self.assertTrue(any(('count(distinct ' in s for s in sqls)), msg='COUNT(DISTINCT <space> missing when aggregating over annotated distinct count SQL: %s' % sqls)

def test_non_count_aggregate_rejects_distinct(self):
    """Non-Count aggregates (e.g., Avg) should raise TypeError when distinct=True is passed."""
    with self.assertRaisesMessage(TypeError, 'Avg does not allow distinct.'):
        Avg('rating', distinct=True)
AggregateTestCase.test_aggregate_count_distinct_sql = test_aggregate_count_distinct_sql
AggregateTestCase.test_annotate_count_distinct_sql = test_annotate_count_distinct_sql
AggregateTestCase.test_values_aggregate_count_distinct_sql = test_values_aggregate_count_distinct_sql
AggregateTestCase.test_count_distinct_case_expression_sql = test_count_distinct_case_expression_sql
AggregateTestCase.test_count_star_distinct_sql = test_count_star_distinct_sql
AggregateTestCase.test_annotate_values_list_count_distinct_sql = test_annotate_values_list_count_distinct_sql
AggregateTestCase.test_grouped_annotation_count_distinct_sql = test_grouped_annotation_count_distinct_sql
AggregateTestCase.test_distinct_in_annotation_on_related = test_distinct_in_annotation_on_related
AggregateTestCase.test_count_distinct_in_subquery_aggregate_sql = test_count_distinct_in_subquery_aggregate_sql
AggregateTestCase.test_non_count_aggregate_rejects_distinct = test_non_count_aggregate_rejects_distinct

def test_count_distinct_sql_aggregate(self):
    with CaptureQueriesContext(connection) as ctx:
        Book.objects.aggregate(distinct_ratings=Count('rating', distinct=True))
    sql = ctx.captured_queries[0]['sql'].upper()
    self.assertIn('COUNT(DISTINCT ', sql)

def test_count_distinct_sql_annotate_query_str(self):
    sql = str(Book.objects.annotate(distinct_count=Count('rating', distinct=True)).query).upper()
    self.assertIn('COUNT(DISTINCT ', sql)

def test_count_distinct_sql_case_expression(self):
    with CaptureQueriesContext(connection) as ctx:
        Book.objects.aggregate(distinct_ratings=Count(Case(When(pages__gt=300, then='rating')), distinct=True))
    sql = ctx.captured_queries[0]['sql'].upper()
    self.assertIn('COUNT(DISTINCT ', sql)

def test_count_distinct_sql_values_aggregate(self):
    with CaptureQueriesContext(connection) as ctx:
        Book.objects.values('rating').aggregate(distinct_count=Count('rating', distinct=True))
    sql = ctx.captured_queries[0]['sql'].upper()
    self.assertIn('COUNT(DISTINCT ', sql)

def test_count_distinct_sql_values_annotate(self):
    sql = str(Book.objects.values('rating').annotate(n=Count('rating', distinct=True)).query).upper()
    self.assertIn('COUNT(DISTINCT ', sql)

def test_count_distinct_star_sql(self):
    with CaptureQueriesContext(connection) as ctx:
        Book.objects.aggregate(n=Count('*', distinct=True))
    sql = ctx.captured_queries[0]['sql'].upper()
    self.assertIn('COUNT(DISTINCT *', sql)

def test_count_distinct_author_books(self):
    with CaptureQueriesContext(connection) as ctx:
        Author.objects.aggregate(n=Count('book', distinct=True))
    sql = ctx.captured_queries[0]['sql'].upper()
    self.assertIn('COUNT(DISTINCT ', sql)

def test_count_distinct_annotate_order_by(self):
    sql = str(Author.objects.annotate(n=Count('book', distinct=True)).order_by('name').query).upper()
    self.assertIn('COUNT(DISTINCT ', sql)

def test_count_distinct_in_join_annotation(self):
    sql = str(Book.objects.annotate(num_authors=Count('authors__id', distinct=True)).query).upper()
    self.assertIn('COUNT(DISTINCT ', sql)

def test_count_repr_options_includes_distinct(self):
    cnt = Count('rating', distinct=True)
    opts = cnt._get_repr_options()
    self.assertIn('distinct', opts)
    self.assertTrue(opts['distinct'])

def test_count_distinct_has_space(self):
    from django.db import connection
    from django.test.utils import CaptureQueriesContext
    from django.db.models import Count
    with CaptureQueriesContext(connection) as ctx:
        Book.objects.aggregate(distinct_count=Count('rating', distinct=True))
    sql = ' '.join((q['sql'] for q in ctx.captured_queries))
    self.assertIn('COUNT(DISTINCT ', sql)
    self.assertNotIn('COUNT(DISTINCT  ', sql)

def test_sum_distinct_has_space(self):
    from django.db import connection
    from django.test.utils import CaptureQueriesContext
    from django.db.models import Sum
    with CaptureQueriesContext(connection) as ctx:
        Book.objects.aggregate(distinct_sum=Sum('price', distinct=True))
    sql = ' '.join((q['sql'] for q in ctx.captured_queries))
    self.assertIn('SUM(DISTINCT ', sql)
    self.assertNotIn('SUM(DISTINCT  ', sql)

def test_avg_distinct_has_space(self):
    from django.db import connection
    from django.test.utils import CaptureQueriesContext
    from django.db.models import Avg
    with CaptureQueriesContext(connection) as ctx:
        Book.objects.aggregate(distinct_avg=Avg('price', distinct=True))
    sql = ' '.join((q['sql'] for q in ctx.captured_queries))
    self.assertIn('AVG(DISTINCT ', sql)
    self.assertNotIn('AVG(DISTINCT  ', sql)

def test_max_distinct_has_space(self):
    from django.db import connection
    from django.test.utils import CaptureQueriesContext
    from django.db.models import Max
    with CaptureQueriesContext(connection) as ctx:
        Book.objects.aggregate(distinct_max=Max('pages', distinct=True))
    sql = ' '.join((q['sql'] for q in ctx.captured_queries))
    self.assertIn('MAX(DISTINCT ', sql)
    self.assertNotIn('MAX(DISTINCT  ', sql)

def test_multiple_distinct_aggregates_each_have_space(self):
    from django.db import connection
    from django.test.utils import CaptureQueriesContext
    from django.db.models import Count, Sum
    with CaptureQueriesContext(connection) as ctx:
        Book.objects.aggregate(Count('rating', distinct=True), Sum('price', distinct=True))
    sql = ' '.join((q['sql'] for q in ctx.captured_queries))
    self.assertIn('COUNT(DISTINCT ', sql)
    self.assertIn('SUM(DISTINCT ', sql)

def test_distinct_in_annotation_has_space(self):
    from django.db import connection
    from django.test.utils import CaptureQueriesContext
    from django.db.models import Count
    with CaptureQueriesContext(connection) as ctx:
        Book.objects.annotate(num_authors=Count('authors', distinct=True)).first()
    sql = ' '.join((q['sql'] for q in ctx.captured_queries))
    self.assertIn('COUNT(DISTINCT ', sql)

def test_distinct_with_case_expression_has_space(self):
    from django.db import connection
    from django.test.utils import CaptureQueriesContext
    from django.db.models import Count, Case, When
    with CaptureQueriesContext(connection) as ctx:
        Book.objects.aggregate(distinct_ratings=Count(Case(When(pages__gt=300, then='rating')), distinct=True))
    sql = ' '.join((q['sql'] for q in ctx.captured_queries))
    self.assertIn('COUNT(DISTINCT ', sql)

def test_values_with_distinct_aggregate_has_space(self):
    from django.db import connection
    from django.test.utils import CaptureQueriesContext
    from django.db.models import Sum
    with CaptureQueriesContext(connection) as ctx:
        Book.objects.values('rating').aggregate(distinct_price=Sum('price', distinct=True))
    sql = ' '.join((q['sql'] for q in ctx.captured_queries))
    self.assertIn('SUM(DISTINCT ', sql)

def test_values_list_annotation_distinct_has_space(self):
    from django.db import connection
    from django.test.utils import CaptureQueriesContext
    from django.db.models import Count
    with CaptureQueriesContext(connection) as ctx:
        list(Book.objects.values_list('rating').annotate(cnt=Count('isbn', distinct=True))[:1])
    sql = ' '.join((q['sql'] for q in ctx.captured_queries))
    self.assertIn('COUNT(DISTINCT ', sql)

def test_distinct_does_not_introduce_double_space(self):
    from django.db import connection
    from django.test.utils import CaptureQueriesContext
    from django.db.models import Count
    with CaptureQueriesContext(connection) as ctx:
        Book.objects.aggregate(distinct_count=Count('rating', distinct=True))
    sql = ' '.join((q['sql'] for q in ctx.captured_queries))
    self.assertRegex(sql, 'DISTINCT [^\\s]')