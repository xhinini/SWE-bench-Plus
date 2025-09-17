from types import SimpleNamespace
import uuid
from django.core import exceptions
from django.test import SimpleTestCase
from django.db.models import fields
from types import SimpleNamespace
import uuid
from django.core import exceptions
from django.test import SimpleTestCase
from django.db.models import fields

class TestUUIDField(SimpleTestCase):

    def setUp(self):
        self.field = fields.UUIDField()

    def test_get_prep_value_from_hex_string(self):
        hexstr = uuid.uuid4().hex
        val = self.field.get_prep_value(hexstr)
        self.assertIsInstance(val, uuid.UUID)
        self.assertEqual(val.hex, hexstr)

    def test_get_prep_value_from_int(self):
        u = uuid.uuid4()
        ival = u.int
        val = self.field.get_prep_value(ival)
        self.assertIsInstance(val, uuid.UUID)
        self.assertEqual(val.int, ival)

from types import SimpleNamespace
from django.utils.functional import lazy
from types import SimpleNamespace
import uuid
from django.test import SimpleTestCase
from django.utils.functional import lazy
from django.db import connection
from django.db.models.fields import UUIDField
FAKE_CONN_NATIVE = SimpleNamespace(features=SimpleNamespace(has_native_uuid_field=True))
FAKE_CONN_NON_NATIVE = SimpleNamespace(features=SimpleNamespace(has_native_uuid_field=False))

class UUIDFieldPrepTests(SimpleTestCase):

    def setUp(self):
        self.field = UUIDField()

    def test_get_prep_value_on_lazy_returns_uuid_instance(self):
        u = uuid.uuid4()
        p = lazy(lambda: u.hex, str)()
        prep = self.field.get_prep_value(p)
        self.assertIsInstance(prep, uuid.UUID)
        self.assertEqual(prep, u)

from django.test import SimpleTestCase
from django.db import connection
from django.core import exceptions
import uuid
from django.utils.functional import lazy
from django.db.models.fields import UUIDField

class UUIDFieldPrepTests(SimpleTestCase):

    def setUp(self):
        self.sample_uuid = uuid.UUID('12345678-1234-5678-1234-567812345678')
        self.hex_no_dashes = self.sample_uuid.hex
        self.int_value = self.sample_uuid.int
        self.field = UUIDField()

    def test_get_prep_value_converts_hex_string_to_uuid(self):
        val = self.field.get_prep_value(self.hex_no_dashes)
        self.assertIsInstance(val, uuid.UUID)
        self.assertEqual(val, self.sample_uuid)

    def test_get_prep_value_converts_int_to_uuid(self):
        val = self.field.get_prep_value(self.int_value)
        self.assertIsInstance(val, uuid.UUID)
        self.assertEqual(val, self.sample_uuid)

    def test_get_prep_value_with_lazy_hex_string(self):
        lazy_hex = lazy(lambda: self.hex_no_dashes, str)()
        val = self.field.get_prep_value(lazy_hex)
        self.assertIsInstance(val, uuid.UUID)
        self.assertEqual(val, self.sample_uuid)

    def test_get_prep_value_with_lazy_int(self):
        lazy_int = lazy(lambda: self.int_value, int)()
        val = self.field.get_prep_value(lazy_int)
        self.assertIsInstance(val, uuid.UUID)
        self.assertEqual(val, self.sample_uuid)

    def test_get_prep_value_invalid_raises(self):
        with self.assertRaises(exceptions.ValidationError):
            self.field.get_prep_value('not-a-valid-uuid')

    def test_get_prep_value_empty_string_invalid_when_empty_strings_not_allowed(self):
        with self.assertRaises(exceptions.ValidationError):
            self.field.get_prep_value('')

import uuid
from django.utils.functional import lazy
import uuid
import unittest
from django.db import connection
from django.utils.functional import lazy
from django.db.models import UUIDField

class UUIDFieldPrepTests(unittest.TestCase):

    def setUp(self):
        self.field = UUIDField()
        self._orig_native = connection.features.has_native_uuid_field

    def tearDown(self):
        connection.features.has_native_uuid_field = self._orig_native

    def test_get_prep_value_converts_hex_string_to_uuid(self):
        hex_str = uuid.uuid4().hex
        res = self.field.get_prep_value(hex_str)
        self.assertIsInstance(res, uuid.UUID)
        self.assertEqual(res.hex, hex_str)

from django.test import SimpleTestCase
from django.db import connection
from django.db.models import fields
from django.core import exceptions
import uuid
import types

class UUIDFieldPrepTests(SimpleTestCase):

    def setUp(self):
        self.field = fields.UUIDField()

    def test_get_prep_value_from_hex_without_dashes(self):
        u = uuid.uuid4()
        hex_no_dash = u.hex
        converted = self.field.get_prep_value(hex_no_dash)
        self.assertIsInstance(converted, uuid.UUID)
        self.assertEqual(converted, u)

    def test_get_prep_value_from_hex_with_dashes(self):
        u = uuid.uuid4()
        hex_with_dash = str(u)
        converted = self.field.get_prep_value(hex_with_dash)
        self.assertIsInstance(converted, uuid.UUID)
        self.assertEqual(converted, u)

    def test_get_prep_value_from_int(self):
        u = uuid.uuid4()
        converted = self.field.get_prep_value(u.int)
        self.assertIsInstance(converted, uuid.UUID)
        self.assertEqual(converted, u)

    def test_get_prep_value_invalid_raises_validation_error(self):
        invalid = 'not-a-uuid'
        with self.assertRaises(exceptions.ValidationError):
            self.field.get_prep_value(invalid)