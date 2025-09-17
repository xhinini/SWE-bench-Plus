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