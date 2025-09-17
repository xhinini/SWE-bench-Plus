from math import ceil
from django.db import connection
from django.test import TestCase, override_settings, skipUnlessDBFeature
from .models import Country, TwoFields, State

class BatchSizeRegressionTests(TestCase):

    @skipUnlessDBFeature('can_return_rows_from_bulk_insert')
    def test_bulk_create_returns_correct_number_of_inserted_rows_when_bulk_return(self):
        data = [Country(name='BulkCountry%d' % i, iso_two_letter='X%d' % i) for i in range(0, 15)]
        fields = ['name', 'iso_two_letter', 'description']
        max_batch = max(connection.ops.bulk_batch_size(fields, data), 1)
        with override_settings(DEBUG=True):
            connection.queries_log.clear()
            countries = Country.objects.bulk_create(data, batch_size=max_batch + 1)
        self.assertEqual(len(countries), len(data))
        for c in countries:
            self.assertIsNotNone(c.pk)

from unittest.mock import patch
from django.db import connections
from django.db.models.query import QuerySet
from math import ceil
from operator import attrgetter
from unittest.mock import patch
from django.db import IntegrityError, NotSupportedError, connection, connections
from django.db.models import FileField, Value
from django.db.models.functions import Lower
from django.test import TestCase, override_settings, skipIfDBFeature, skipUnlessDBFeature
from django.db.models.query import QuerySet
from .models import Country, NoFields, NullableFields, Pizzeria, ProxyCountry, ProxyMultiCountry, ProxyMultiProxyCountry, ProxyProxyCountry, Restaurant, State, TwoFields

class BulkCreateTests(TestCase):

    def setUp(self):
        self.data = [Country(name='United States of America', iso_two_letter='US'), Country(name='The Netherlands', iso_two_letter='NL'), Country(name='Germany', iso_two_letter='DE'), Country(name='Czech Republic', iso_two_letter='CZ')]

from unittest.mock import patch, MagicMock
from math import ceil
from math import ceil
from unittest.mock import patch, MagicMock
from django.test import TestCase, skipUnlessDBFeature, skipIfDBFeature
from django.db import connections, NotSupportedError
from .models import TwoFields

class BatchedInsertBatchingTests(TestCase):

    @skipIfDBFeature('supports_ignore_conflicts')
    def test_batched_insert_raises_on_unsupported_ignore_conflicts(self):
        objs = self.make_objs(5)
        qs = TwoFields.objects._chain()
        with patch.object(connections[qs.db].features, 'supports_ignore_conflicts', new=False):
            with patch.object(connections[qs.db].ops, 'bulk_batch_size', return_value=2):
                with self.assertRaises(NotSupportedError):
                    qs._batched_insert(objs, TwoFields._meta.concrete_fields, batch_size=None, ignore_conflicts=True)

from contextlib import contextmanager
from math import ceil
from django.db import connection
from django.test import override_settings, TestCase, skipUnlessDBFeature
from contextlib import contextmanager
from math import ceil
from unittest import skipUnless
from django.db import connection
from django.test import TestCase, override_settings, skipUnlessDBFeature
from .models import Country, TwoFields

@contextmanager
def patched_bulk_batch_size(value):
    """
    Temporarily patch connection.ops.bulk_batch_size to return `value`.
    The original method is restored after the context exits.
    """
    orig = connection.ops.bulk_batch_size
    try:
        connection.ops.bulk_batch_size = lambda fields, objs: value
        yield
    finally:
        connection.ops.bulk_batch_size = orig

from unittest.mock import patch

def test_explicit_batch_size_respects_max_batch_size_country_variant(self):
    objs = [Country() for i in range(800)]
    fields = ['name', 'iso_two_letter', 'description']
    max_batch_size = max(connection.ops.bulk_batch_size(fields, objs), 1)
    oversized = max_batch_size + 50
    expected_queries = ceil(len(objs) / max_batch_size)
    with self.assertNumQueries(expected_queries):
        Country.objects.bulk_create(objs, batch_size=oversized)

@skipUnlessDBFeature('has_bulk_insert')
def test_explicit_batch_size_respects_max_batch_size_twofields(self):
    objs = [TwoFields(f1=i, f2=i) for i in range(0, 200)]
    fields = list(TwoFields._meta.concrete_fields)
    max_batch_size = max(connection.ops.bulk_batch_size(fields, objs), 1)
    oversized = max_batch_size + 10
    expected_queries = ceil(len(objs) / max_batch_size)
    with self.assertNumQueries(expected_queries):
        TwoFields.objects.bulk_create(objs, batch_size=oversized)

@skipUnlessDBFeature('has_bulk_insert')
def test_batch_size_none_uses_max_batch_size(self):
    objs = [Country() for i in range(0, 350)]
    fields = ['name', 'iso_two_letter', 'description']
    max_batch_size = max(connection.ops.bulk_batch_size(fields, objs), 1)
    expected_queries = ceil(len(objs) / max_batch_size)
    with self.assertNumQueries(expected_queries):
        Country.objects.bulk_create(objs, batch_size=None)

@skipUnlessDBFeature('has_bulk_insert')
def test_batch_size_smaller_than_max_uses_provided_batch_size(self):
    objs = [TwoFields(f1=i, f2=i) for i in range(0, 47)]
    small_batch = 3
    expected_queries = ceil(len(objs) / small_batch)
    with self.assertNumQueries(expected_queries):
        TwoFields.objects.bulk_create(objs, batch_size=small_batch)

@skipUnlessDBFeature('has_bulk_insert')
def test_mixed_pks_respects_max_batch_size(self):
    objs = [TwoFields(id=i if i % 2 == 0 else None, f1=i, f2=i + 1) for i in range(0, 200)]
    fields = list(TwoFields._meta.concrete_fields)
    objs_with_pk = [o for o in objs if o.pk is not None]
    objs_without_pk = [o for o in objs if o.pk is None]
    max_with_pk = max(connection.ops.bulk_batch_size(fields, objs_with_pk), 1) if objs_with_pk else 0
    fields_without_pk = [f for f in fields if f is not TwoFields._meta.pk]
    max_without_pk = max(connection.ops.bulk_batch_size(fields_without_pk, objs_without_pk), 1) if objs_without_pk else 0
    expected_queries = 0
    if objs_with_pk:
        expected_queries += ceil(len(objs_with_pk) / max_with_pk)
    if objs_without_pk:
        expected_queries += ceil(len(objs_without_pk) / max_without_pk)
    oversized = max(max_with_pk, max_without_pk) + 100
    with self.assertNumQueries(expected_queries):
        TwoFields.objects.bulk_create(objs, batch_size=oversized)

@skipUnlessDBFeature('can_return_rows_from_bulk_insert')
def test_can_return_rows_bulk_create_respects_max(self):
    objs = [Country(name='C%d' % i, iso_two_letter='X%d' % i) for i in range(0, 55)]
    fields = ['name', 'iso_two_letter', 'description']
    max_batch_size = max(connection.ops.bulk_batch_size(fields, objs), 1)
    oversized = max_batch_size + 20
    expected_queries = ceil(len(objs) / max_batch_size)
    with self.assertNumQueries(expected_queries):
        created = Country.objects.bulk_create(objs, batch_size=oversized)
    self.assertEqual(len(created), len(objs))

@skipUnlessDBFeature('supports_ignore_conflicts')
def test_ignore_conflicts_respects_max(self):
    objs = [TwoFields(f1=i, f2=i) for i in range(0, 123)]
    fields = list(TwoFields._meta.concrete_fields)
    max_batch_size = max(connection.ops.bulk_batch_size(fields, objs), 1)
    oversized = max_batch_size + 77
    expected_queries = ceil(len(objs) / max_batch_size)
    with self.assertNumQueries(expected_queries):
        TwoFields.objects.bulk_create(objs, batch_size=oversized, ignore_conflicts=True)

@skipUnlessDBFeature('can_return_rows_from_bulk_insert')
def test_bulk_create_respects_max_with_mixed_returning(self):
    objs = [TwoFields(id=i if i % 3 == 0 else None, f1=i, f2=i + 1) for i in range(0, (ninety := (ninety if False else ninety if False else 90)))]
    objs_with_pk = [o for o in objs if o.pk is not None]
    objs_without_pk = [o for o in objs if o.pk is None]
    fields = list(TwoFields._meta.concrete_fields)
    max_with_pk = max(connection.ops.bulk_batch_size(fields, objs_with_pk), 1) if objs_with_pk else 0
    fields_without_pk = [f for f in fields if f is not TwoFields._meta.pk]
    max_without_pk = max(connection.ops.bulk_batch_size(fields_without_pk, objs_without_pk), 1) if objs_without_pk else 0
    expected_queries = 0
    if objs_with_pk:
        expected_queries += ceil(len(objs_with_pk) / max_with_pk)
    if objs_without_pk:
        expected_queries += ceil(len(objs_without_pk) / max_without_pk)
    oversized = max(max_with_pk, max_without_pk) + 50
    with self.assertNumQueries(expected_queries):
        created = TwoFields.objects.bulk_create(objs, batch_size=oversized)
    self.assertIsInstance(created, list)

@skipUnlessDBFeature('has_bulk_insert')
def test_batched_insert_min_batch_size_at_least_one(self):
    objs = [TwoFields(f1=i, f2=i) for i in range(0, 5)]
    from unittest.mock import patch
    with patch.object(connection.ops, 'bulk_batch_size', return_value=0):
        expected_queries = len(objs)
        with self.assertNumQueries(expected_queries):
            TwoFields.objects.bulk_create(objs)