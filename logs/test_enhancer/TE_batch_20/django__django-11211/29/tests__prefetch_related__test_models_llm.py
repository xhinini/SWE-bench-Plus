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

from types import SimpleNamespace
import uuid
import unittest
from types import SimpleNamespace
from django.core import exceptions
from django.db.models.fields import UUIDField

class UUIDFieldPrepTests(unittest.TestCase):

    def setUp(self):
        self.field = UUIDField()

    def test_get_prep_value_converts_hex_string_to_uuid(self):
        hex_val = uuid.uuid4().hex
        result = self.field.get_prep_value(hex_val)
        self.assertIsInstance(result, uuid.UUID)
        self.assertEqual(result.hex, hex_val)

    def test_get_prep_value_converts_dashed_string_to_uuid(self):
        dashed = str(uuid.uuid4())
        result = self.field.get_prep_value(dashed)
        self.assertIsInstance(result, uuid.UUID)
        self.assertEqual(result.hex, dashed.replace('-', ''))

    def test_get_db_prep_value_with_native_uuid_field_returns_uuid_instance(self):
        conn = SimpleNamespace(features=SimpleNamespace(has_native_uuid_field=True))
        hex_val = uuid.uuid4().hex
        prepped = self.field.get_prep_value(hex_val)
        self.assertIsInstance(prepped, uuid.UUID)
        db_val = self.field.get_db_prep_value(prepped, conn, prepared=True)
        self.assertIsInstance(db_val, uuid.UUID)
        self.assertEqual(db_val.hex, hex_val)

    def test_get_db_prep_value_without_native_uuid_field_returns_hex(self):
        conn = SimpleNamespace(features=SimpleNamespace(has_native_uuid_field=False))
        dashed = str(uuid.uuid4())
        prepped = self.field.get_prep_value(dashed)
        self.assertIsInstance(prepped, uuid.UUID)
        db_val = self.field.get_db_prep_value(prepped, conn, prepared=True)
        self.assertIsInstance(db_val, str)
        self.assertEqual(db_val, prepped.hex)
if __name__ == '__main__':
    unittest.main()

from types import SimpleNamespace
from django.utils.functional import lazy
from types import SimpleNamespace
import uuid
from django.test import SimpleTestCase
from django.utils.functional import lazy
from django.db.models.fields import UUIDField

class UUIDFieldPrepTests(SimpleTestCase):

    def setUp(self):
        self.field = UUIDField()

    def test_get_prep_value_from_hex_string_returns_uuid(self):
        u = uuid.uuid4()
        hex_str = u.hex
        result = self.field.get_prep_value(hex_str)
        self.assertIsInstance(result, uuid.UUID)
        self.assertEqual(result, u)

    def test_get_prep_value_from_int_returns_uuid(self):
        u = uuid.uuid4()
        result = self.field.get_prep_value(u.int)
        self.assertIsInstance(result, uuid.UUID)
        self.assertEqual(result.int, u.int)

    def test_get_prep_value_from_promise_hex_returns_uuid(self):
        u = uuid.uuid4()
        hex_str = u.hex
        lazy_val = lazy(lambda: hex_str, str)()
        self.assertNotIsInstance(lazy_val, uuid.UUID)
        result = self.field.get_prep_value(lazy_val)
        self.assertIsInstance(result, uuid.UUID)
        self.assertEqual(result, u)

    def test_get_prep_value_from_promise_int_returns_uuid(self):
        u = uuid.uuid4()
        lazy_val = lazy(lambda: u.int, int)()
        result = self.field.get_prep_value(lazy_val)
        self.assertIsInstance(result, uuid.UUID)
        self.assertEqual(result.int, u.int)

from django.test import SimpleTestCase
from django.db.models.fields import UUIDField
from django.core.exceptions import ValidationError
import uuid
from django.test import SimpleTestCase
from django.db.models.fields import UUIDField
from django.core.exceptions import ValidationError
import uuid

class UUIDFieldGetPrepValueTests(SimpleTestCase):

    def setUp(self):
        self.field = UUIDField()

    def test_get_prep_value_hex_without_dashes_lowercase(self):
        u = uuid.uuid4()
        hexstr = u.hex
        got = self.field.get_prep_value(hexstr)
        self.assertIsInstance(got, uuid.UUID)
        self.assertEqual(got, u)

    def test_get_prep_value_hex_without_dashes_uppercase(self):
        u = uuid.uuid4()
        hexstr_upper = u.hex.upper()
        got = self.field.get_prep_value(hexstr_upper)
        self.assertIsInstance(got, uuid.UUID)
        self.assertEqual(got, u)

    def test_get_prep_value_int(self):
        u = uuid.uuid4()
        got = self.field.get_prep_value(u.int)
        self.assertIsInstance(got, uuid.UUID)
        self.assertEqual(got, u)

    def test_get_prep_value_invalid_string_raises(self):
        with self.assertRaises(ValidationError):
            self.field.get_prep_value('not-a-uuid')

    def test_get_prep_value_memoryview_raises(self):
        b = uuid.uuid4().hex.encode('ascii')
        with self.assertRaises(ValidationError):
            self.field.get_prep_value(memoryview(b))

from django.test import SimpleTestCase
from django.utils.functional import lazy
from django.utils.translation import gettext_lazy as _
from django.core import exceptions
from django.db.models import fields
import uuid
from django.test import SimpleTestCase
from django.utils.functional import lazy
from django.utils.translation import gettext_lazy as _
from django.core import exceptions
from django.db.models import fields
import uuid

class UUIDFieldGetPrepValueTests(SimpleTestCase):

    def setUp(self):
        self.field = fields.UUIDField()

    def test_get_prep_value_with_lazy_hex_string(self):
        u = uuid.uuid4()
        lazy_hex = lazy(lambda: u.hex, str)()
        res = self.field.get_prep_value(lazy_hex)
        self.assertIsInstance(res, uuid.UUID)
        self.assertEqual(res, u)

    def test_get_prep_value_with_lazy_int(self):
        u = uuid.uuid4()
        lazy_int = lazy(lambda: u.int, int)()
        res = self.field.get_prep_value(lazy_int)
        self.assertIsInstance(res, uuid.UUID)
        self.assertEqual(res, u)

    def test_get_prep_value_with_plain_hex_string(self):
        u = uuid.uuid4()
        res = self.field.get_prep_value(u.hex)
        self.assertIsInstance(res, uuid.UUID)
        self.assertEqual(res, u)

    def test_get_prep_value_with_plain_int(self):
        u = uuid.uuid4()
        res = self.field.get_prep_value(u.int)
        self.assertIsInstance(res, uuid.UUID)
        self.assertEqual(res, u)

    def test_get_prep_value_with_invalid_lazy_string_raises_validation_error(self):
        bad_lazy = lazy(lambda: 'not-a-uuid', str)()
        with self.assertRaises(exceptions.ValidationError):
            self.field.get_prep_value(bad_lazy)

    def test_get_prep_value_with_gettext_lazy_hex(self):
        u = uuid.uuid4()
        lazy_translated = _(u.hex)
        res = self.field.get_prep_value(lazy_translated)
        self.assertIsInstance(res, uuid.UUID)
        self.assertEqual(res, u)

from django.test import SimpleTestCase
from django.db.models.fields import UUIDField
from django.db import connections
from django.utils.translation import gettext_lazy as _
import uuid
from django.test import SimpleTestCase
from django.db.models.fields import UUIDField
from django.db import connections
from django.utils.translation import gettext_lazy as _
import uuid

class UUIDFieldPrepValueTests(SimpleTestCase):

    def setUp(self):
        self.field = UUIDField()

    def test_get_prep_value_hyphenated_string(self):
        s = '12345678-1234-5678-1234-567812345678'
        got = self.field.get_prep_value(s)
        self.assertIsInstance(got, uuid.UUID)
        self.assertEqual(got, uuid.UUID(s))

    def test_get_prep_value_hex_string(self):
        hex_s = '12345678123456781234567812345678'
        got = self.field.get_prep_value(hex_s)
        self.assertIsInstance(got, uuid.UUID)
        self.assertEqual(got, uuid.UUID(hex=hex_s))

    def test_get_prep_value_int(self):
        u = uuid.uuid4()
        got = self.field.get_prep_value(u.int)
        self.assertIsInstance(got, uuid.UUID)
        self.assertEqual(got, uuid.UUID(int=u.int))

    def test_get_prep_value_with_promise_hyphenated(self):
        s = '12345678-1234-5678-1234-567812345678'
        promise = _(s)
        got = self.field.get_prep_value(promise)
        self.assertIsInstance(got, uuid.UUID)
        self.assertEqual(got, uuid.UUID(s))

    def test_get_prep_value_with_promise_hex(self):
        hex_s = '12345678123456781234567812345678'
        promise = _(hex_s)
        got = self.field.get_prep_value(promise)
        self.assertIsInstance(got, uuid.UUID)
        self.assertEqual(got, uuid.UUID(hex=hex_s))

from types import SimpleNamespace
from types import SimpleNamespace
import uuid
from django.test import SimpleTestCase
from django.db.models.fields import UUIDField
from django.core import exceptions

class UUIDFieldPrepTests(SimpleTestCase):

    def setUp(self):
        self.field = UUIDField()

    def test_get_prep_value_with_hex_with_dashes(self):
        u = uuid.uuid4()
        s = str(u)
        prep = self.field.get_prep_value(s)
        self.assertIsInstance(prep, uuid.UUID)
        self.assertEqual(prep, u)

    def test_get_prep_value_with_hex_without_dashes(self):
        u = uuid.uuid4()
        s = u.hex
        prep = self.field.get_prep_value(s)
        self.assertIsInstance(prep, uuid.UUID)
        self.assertEqual(prep, u)

    def test_get_prep_value_with_int(self):
        u = uuid.uuid4()
        i = u.int
        prep = self.field.get_prep_value(i)
        self.assertIsInstance(prep, uuid.UUID)
        self.assertEqual(prep.int, i)

    def test_get_prep_value_raises_on_invalid(self):
        with self.assertRaises(exceptions.ValidationError):
            self.field.get_prep_value('not-a-uuid')

from unittest.mock import patch
import uuid
from django.test import SimpleTestCase
from django.db import connection
from django.core.exceptions import ValidationError
from django.db.models import fields
from unittest.mock import patch
import uuid
from django.test import SimpleTestCase
from django.db import connection
from django.core.exceptions import ValidationError
from django.db.models import fields

class UUIDFieldPrepTests(SimpleTestCase):

    def test_get_prep_value_converts_hex_string_without_dashes_to_uuid(self):
        f = fields.UUIDField()
        hex32 = uuid.UUID(int=0).hex
        result = f.get_prep_value(hex32)
        self.assertIsInstance(result, uuid.UUID)
        self.assertEqual(result.hex, hex32)

    def test_get_prep_value_converts_hex_string_with_dashes(self):
        f = fields.UUIDField()
        dashed = '550e8400-e29b-41d4-a716-446655440000'
        result = f.get_prep_value(dashed)
        self.assertIsInstance(result, uuid.UUID)
        self.assertEqual(str(result), dashed)

    def test_get_prep_value_converts_int_to_uuid(self):
        f = fields.UUIDField()
        val_int = 12345678901234567890
        result = f.get_prep_value(val_int)
        self.assertIsInstance(result, uuid.UUID)
        self.assertEqual(result.int, val_int)

import uuid
from django.core import exceptions
from django.test import SimpleTestCase
from django.db.models.fields import UUIDField

class UUIDFieldPrepTests(SimpleTestCase):

    def setUp(self):
        self.field = UUIDField()

    def test_get_prep_value_with_dashed_string(self):
        u = uuid.uuid4()
        dashed = str(u)
        result = self.field.get_prep_value(dashed)
        self.assertIsInstance(result, uuid.UUID)
        self.assertEqual(result, u)

    def test_get_prep_value_with_hex_string_no_dashes(self):
        u = uuid.uuid4()
        hexstr = u.hex
        result = self.field.get_prep_value(hexstr)
        self.assertIsInstance(result, uuid.UUID)
        self.assertEqual(result, u)

    def test_get_prep_value_with_int(self):
        u = uuid.uuid4()
        as_int = u.int
        result = self.field.get_prep_value(as_int)
        self.assertIsInstance(result, uuid.UUID)
        self.assertEqual(result, u)

    def test_get_prep_value_raises_on_invalid_string(self):
        with self.assertRaises(exceptions.ValidationError):
            self.field.get_prep_value('not-a-uuid')

    def test_get_prep_value_raises_on_empty_string(self):
        with self.assertRaises(exceptions.ValidationError):
            self.field.get_prep_value('')

    def test_get_prep_value_preserves_uuid_type_for_valid_inputs(self):
        u = uuid.uuid4()
        variants = [str(u), u.hex, u.hex.upper()]
        for v in variants:
            res = self.field.get_prep_value(v)
            self.assertIsInstance(res, uuid.UUID)
            self.assertEqual(res, u)

    def test_get_prep_value_invalid_int_raises(self):
        with self.assertRaises(exceptions.ValidationError):
            self.field.get_prep_value(-1)

from django.db import connection
from django.utils.functional import lazy
from unittest import mock
from unittest import mock
from django.test import SimpleTestCase
from django.db import connection
from django.utils.functional import lazy
from django.core import exceptions
from django.db.models.fields import UUIDField
import uuid

class UUIDFieldPrepTests(SimpleTestCase):

    def setUp(self):
        self.field = UUIDField()

    def test_get_prep_value_unwraps_lazy_and_returns_uuid(self):
        u = uuid.uuid4()
        lazy_hex = lazy(lambda: u.hex, str)()
        prep = self.field.get_prep_value(lazy_hex)
        self.assertIsInstance(prep, uuid.UUID)
        self.assertEqual(prep, u)

import types
import types
import unittest
import uuid
from django.core import exceptions
from django.db.models.fields import UUIDField

class UUIDFieldPrepTests(unittest.TestCase):

    def setUp(self):
        self.field = UUIDField()

    def test_get_prep_value_int(self):
        u = uuid.uuid4()
        result = self.field.get_prep_value(u.int)
        self.assertIsInstance(result, uuid.UUID)
        self.assertEqual(result, u)

    def test_get_prep_value_hex_without_dashes(self):
        u = uuid.uuid4()
        hex32 = u.hex
        result = self.field.get_prep_value(hex32)
        self.assertIsInstance(result, uuid.UUID)
        self.assertEqual(result, u)

    def test_get_prep_value_uppercase_hex(self):
        u = uuid.uuid4()
        hex_upper = u.hex.upper()
        result = self.field.get_prep_value(hex_upper)
        self.assertIsInstance(result, uuid.UUID)
        self.assertEqual(result, u)

    def test_get_prep_value_invalid_length_raises(self):
        with self.assertRaises(exceptions.ValidationError):
            self.field.get_prep_value('deadbeef')

    def test_get_prep_value_rejects_non_hex_nor_int(self):
        with self.assertRaises(exceptions.ValidationError):
            self.field.get_prep_value('not-a-uuid')
if __name__ == '__main__':
    unittest.main()

from django.test import SimpleTestCase
from django.db import connection
from django.db.models.fields import UUIDField
import uuid

class UUIDFieldPrepTests(SimpleTestCase):

    def setUp(self):
        self.field = UUIDField()

    def test_get_prep_value_accepts_hex_string_without_dashes(self):
        u = uuid.uuid4()
        hex_str = u.hex
        prepared = self.field.get_prep_value(hex_str)
        self.assertIsInstance(prepared, uuid.UUID)
        self.assertEqual(prepared, u)

    def test_get_prep_value_accepts_dashed_string(self):
        u = uuid.uuid4()
        dashed = str(u)
        prepared = self.field.get_prep_value(dashed)
        self.assertIsInstance(prepared, uuid.UUID)
        self.assertEqual(prepared, u)

    def test_get_prep_value_accepts_int(self):
        u = uuid.uuid4()
        u_int = u.int
        prepared = self.field.get_prep_value(u_int)
        self.assertIsInstance(prepared, uuid.UUID)
        self.assertEqual(prepared, u)

    def test_get_db_prep_value_prepared_true_after_get_prep_value_hex_string(self):
        u = uuid.uuid4()
        hex_str = u.hex
        prepped = self.field.get_prep_value(hex_str)
        self.assertIsInstance(prepped, uuid.UUID)
        db_val = self.field.get_db_prep_value(prepped, connection, prepared=True)
        expected = self._db_value_for_uuid(prepped)
        self.assertEqual(db_val, expected)

    def test_get_db_prep_value_prepared_true_after_get_prep_value_dashed_string(self):
        u = uuid.uuid4()
        dashed = str(u)
        prepped = self.field.get_prep_value(dashed)
        self.assertIsInstance(prepped, uuid.UUID)
        db_val = self.field.get_db_prep_value(prepped, connection, prepared=True)
        expected = self._db_value_for_uuid(prepped)
        self.assertEqual(db_val, expected)