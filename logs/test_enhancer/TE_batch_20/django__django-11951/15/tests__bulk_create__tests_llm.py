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