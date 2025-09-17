def test_add_field_primary_key_integerfield_triggers_remake(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = IntegerField(primary_key=True)
    new_field.set_attributes_from_name('new_pk_int')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] or 'DROP TABLE' in q['sql'] for q in ctx.captured_queries)))

def test_add_field_primary_key_autofield_triggers_remake(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = AutoField(primary_key=True)
    new_field.set_attributes_from_name('new_pk_auto')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] or 'DROP TABLE' in q['sql'] for q in ctx.captured_queries)))

def test_add_field_primary_key_bigautofield_triggers_remake(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = BigAutoField(primary_key=True)
    new_field.set_attributes_from_name('new_pk_bigauto')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] or 'DROP TABLE' in q['sql'] for q in ctx.captured_queries)))

def test_add_field_primary_key_smallautofield_triggers_remake(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = SmallAutoField(primary_key=True)
    new_field.set_attributes_from_name('new_pk_smallauto')
    new_field.model = Author
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] or 'DROP TABLE' in q['sql'] for q in ctx.captured_queries)))

def test_add_field_primary_key_charfield_triggers_remake(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = CharField(max_length=50, primary_key=True)
    new_field.set_attributes_from_name('new_pk_char')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] or 'DROP TABLE' in q['sql'] for q in ctx.captured_queries)))

def test_add_field_primary_key_slugfield_triggers_remake(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = SlugField(primary_key=True)
    new_field.set_attributes_from_name('new_pk_slug')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] or 'DROP TABLE' in q['sql'] for q in ctx.captured_queries)))

def test_add_field_primary_key_uuidfield_triggers_remake(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = UUIDField(primary_key=True)
    new_field.set_attributes_from_name('new_pk_uuid')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] or 'DROP TABLE' in q['sql'] for q in ctx.captured_queries)))

def test_add_field_primary_key_bigintegerfield_triggers_remake(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = BigIntegerField(primary_key=True)
    new_field.set_attributes_from_name('new_pk_bigint')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] or 'DROP TABLE' in q['sql'] for q in ctx.captured_queries)))

def test_add_field_primary_key_positiveintegerfield_triggers_remake(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = PositiveIntegerField(primary_key=True)
    new_field.set_attributes_from_name('new_pk_positiveint')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] or 'DROP TABLE' in q['sql'] for q in ctx.captured_queries)))

def test_add_field_primary_key_decimalfield_triggers_remake(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = DecimalField(max_digits=5, decimal_places=2, primary_key=True)
    new_field.set_attributes_from_name('new_pk_decimal')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] or 'DROP TABLE' in q['sql'] for q in ctx.captured_queries)))

import unittest
from django.db import connection
from django.db.models import AutoField, BigAutoField, BigIntegerField, CharField, IntegerField, PositiveIntegerField, SmallAutoField, SlugField, UUIDField
from django.test import TransactionTestCase, skipUnlessDBFeature
from .models import Author

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
class AddPrimaryKeyFieldSQLiteTests(TransactionTestCase):
    """
    Regression tests for sqlite3.schema.DatabaseSchemaEditor.add_field ensuring
    primary_key fields trigger a table remake rather than an ALTER TABLE ADD COLUMN.
    """
    available_apps = []

    def tearDown(self):
        try:
            with connection.schema_editor() as editor:
                editor.delete_model(Author)
        except Exception:
            pass

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_autofield_triggers_remake(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = AutoField(primary_key=True)
    new_field.set_attributes_from_name('new_pk_auto')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_integerfield_triggers_remake(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = IntegerField(primary_key=True)
    new_field.set_attributes_from_name('new_pk_int')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_bigautofield_triggers_remake(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = BigAutoField(primary_key=True)
    new_field.set_attributes_from_name('new_pk_bigauto')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_smallautofield_triggers_remake(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = SmallAutoField(primary_key=True)
    new_field.set_attributes_from_name('new_pk_smallauto')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_uuidfield_triggers_remake(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = UUIDField(primary_key=True)
    new_field.set_attributes_from_name('new_pk_uuid')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_charfield_triggers_remake(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = CharField(max_length=50, primary_key=True)
    new_field.set_attributes_from_name('new_pk_char')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_slugfield_triggers_remake(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = SlugField(max_length=50, primary_key=True)
    new_field.set_attributes_from_name('new_pk_slug')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_positiveintegerfield_triggers_remake(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = PositiveIntegerField(primary_key=True)
    new_field.set_attributes_from_name('new_pk_positive_int')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_smallintegerfield_triggers_remake(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = SmallIntegerField(primary_key=True)
    new_field.set_attributes_from_name('new_pk_small_int')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_bigintegerfield_triggers_remake(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = BigIntegerField(primary_key=True)
    new_field.set_attributes_from_name('new_pk_big_int')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))

from django.db import connection
from django.test import TransactionTestCase
from django.db.models import CharField, IntegerField, BooleanField, TextField, BinaryField, DateField, DateTimeField, TimeField, DecimalField, DurationField
from django.test.utils import CaptureQueriesContext

class AddNullableFieldTests(TransactionTestCase):
    available_apps = []

    def setUp(self):
        pass

    def tearDown(self):
        with connection.schema_editor() as editor:
            try:

                class Dummy:
                    pass
                editor.execute('DROP TABLE IF EXISTS schema_author')
            except Exception:
                pass

import unittest
from django.db import connection
from django.db.models import AutoField, BigAutoField, BigIntegerField, CharField, IntegerField, PositiveIntegerField, SmallAutoField, SlugField, UUIDField
from django.test.utils import isolate_apps
from django.test import skipUnlessDBFeature
from django.test.utils import CaptureQueriesContext
import unittest

class SQLiteAddFieldPrimaryKeyTests(unittest.TestCase):
    """
    SQLite-specific tests ensuring add_field remakes the table when the added
    field is a primary key. These are skipped unless the backend is SQLite.
    """

    def _get_base_model(self):
        from django.db.models import Model
        return Model

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_autofield_sqlite(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = AutoField(primary_key=True)
    new_field.set_attributes_from_name('new_pk_autofield')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_bigautofield_sqlite(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = BigAutoField(primary_key=True)
    new_field.set_attributes_from_name('new_pk_bigautofield')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_integerfield_sqlite(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = IntegerField(primary_key=True)
    new_field.set_attributes_from_name('new_pk_integerfield')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_bigintegerfield_sqlite(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = BigIntegerField(primary_key=True)
    new_field.set_attributes_from_name('new_pk_bigintegerfield')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_charfield_sqlite(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = CharField(primary_key=True, max_length=50)
    new_field.set_attributes_from_name('new_pk_charfield')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_one_to_onefield_sqlite(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
        editor.create_model(Book)
    new_field = OneToOneField(Author, CASCADE, primary_key=True)
    new_field.set_attributes_from_name('author_o2o_pk')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Book, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_after_rows_sqlite(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    Author.objects.create(name='A')
    Author.objects.create(name='B')
    new_field = AutoField(primary_key=True)
    new_field.set_attributes_from_name('new_pk_after_rows')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_with_nullable_sqlite(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = IntegerField(primary_key=True, null=True)
    new_field.set_attributes_from_name('new_pk_nullable')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_many_variations_sqlite(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    variants = [AutoField(primary_key=True), BigAutoField(primary_key=True), IntegerField(primary_key=True), CharField(primary_key=True, max_length=20)]
    for idx, field in enumerate(variants):
        field.set_attributes_from_name('pk_variant_%d' % idx)
        with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
            editor.add_field(Author, field)
        self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))

from django.db import connection
from django.test import TransactionTestCase
from django.test.utils import CaptureQueriesContext, isolate_apps
from django.db.models import AutoField, IntegerField, BigAutoField, CharField, UUIDField, OneToOneField, Model, ForeignKey, CASCADE
import uuid
from django.db import connection
from django.test import TransactionTestCase
from django.test.utils import CaptureQueriesContext, isolate_apps
from django.db.models import AutoField, IntegerField, BigAutoField, CharField, UUIDField, OneToOneField, Model, ForeignKey, CASCADE
import uuid

def get_primary_key(table):
    with connection.cursor() as cursor:
        return connection.introspection.get_primary_key_column(cursor, table)

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_primary_key_autofield_triggers_remake(self):
    with connection.schema_editor() as editor:
        editor.create_model(Tag)
    new_field = AutoField(primary_key=True)
    new_field.set_attributes_from_name('new_id')
    new_field.model = Tag
    id_field = Tag._meta.get_field('id')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.remove_field(Tag, id_field)
        editor.add_field(Tag, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'].upper() for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_primary_key_bigautofield_triggers_remake(self):
    with connection.schema_editor() as editor:
        editor.create_model(Tag)
    new_field = BigAutoField(primary_key=True)
    new_field.set_attributes_from_name('new_id')
    new_field.model = Tag
    id_field = Tag._meta.get_field('id')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.remove_field(Tag, id_field)
        editor.add_field(Tag, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'].upper() for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_primary_key_integerfield_triggers_remake(self):
    with connection.schema_editor() as editor:
        editor.create_model(Tag)
    new_field = IntegerField(primary_key=True)
    new_field.set_attributes_from_name('new_id')
    new_field.model = Tag
    id_field = Tag._meta.get_field('id')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.remove_field(Tag, id_field)
        editor.add_field(Tag, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'].upper() for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_primary_key_charfield_triggers_remake(self):
    with connection.schema_editor() as editor:
        editor.create_model(Tag)
    new_field = CharField(max_length=50, primary_key=True)
    new_field.set_attributes_from_name('new_id')
    new_field.model = Tag
    id_field = Tag._meta.get_field('id')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.remove_field(Tag, id_field)
        editor.add_field(Tag, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'].upper() for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_primary_key_uuidfield_triggers_remake(self):
    with connection.schema_editor() as editor:
        editor.create_model(Tag)
    new_field = UUIDField(primary_key=True)
    new_field.set_attributes_from_name('new_id')
    new_field.model = Tag
    id_field = Tag._meta.get_field('id')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.remove_field(Tag, id_field)
        editor.add_field(Tag, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'].upper() for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_primary_key_smallautofield_triggers_remake(self):
    with connection.schema_editor() as editor:
        editor.create_model(Tag)
    new_field = SmallAutoField(primary_key=True)
    new_field.set_attributes_from_name('new_id')
    new_field.model = Tag
    id_field = Tag._meta.get_field('id')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.remove_field(Tag, id_field)
        editor.add_field(Tag, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'].upper() for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_primary_key_smallintegerfield_triggers_remake(self):
    with connection.schema_editor() as editor:
        editor.create_model(Tag)
    new_field = SmallIntegerField(primary_key=True)
    new_field.set_attributes_from_name('new_id')
    new_field.model = Tag
    id_field = Tag._meta.get_field('id')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.remove_field(Tag, id_field)
        editor.add_field(Tag, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'].upper() for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_primary_key_positiveintegerfield_triggers_remake(self):
    with connection.schema_editor() as editor:
        editor.create_model(Tag)
    new_field = PositiveIntegerField(primary_key=True)
    new_field.set_attributes_from_name('new_id')
    new_field.model = Tag
    id_field = Tag._meta.get_field('id')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.remove_field(Tag, id_field)
        editor.add_field(Tag, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'].upper() for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_primary_key_slugfield_triggers_remake(self):
    with connection.schema_editor() as editor:
        editor.create_model(Tag)
    new_field = SlugField(max_length=50, primary_key=True)
    new_field.set_attributes_from_name('new_id')
    new_field.model = Tag
    id_field = Tag._meta.get_field('id')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.remove_field(Tag, id_field)
        editor.add_field(Tag, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'].upper() for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_primary_key_decimalfield_triggers_remake(self):
    with connection.schema_editor() as editor:
        editor.create_model(Tag)
    new_field = DecimalField(max_digits=5, decimal_places=2, primary_key=True)
    new_field.set_attributes_from_name('new_id')
    new_field.model = Tag
    id_field = Tag._meta.get_field('id')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.remove_field(Tag, id_field)
        editor.add_field(Tag, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'].upper() for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_nullable_integer_field_does_not_remake_or_raise(self):
    """
    Adding a nullable IntegerField should not remake the table and should
    not raise (regression guard against accidental .one_to_one access).
    """
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = IntegerField(null=True)
    new_field.set_attributes_from_name('nullable_integer')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    sqls = [q['sql'] for q in ctx.captured_queries]
    self.assertFalse(any(('CREATE TABLE' in s for s in sqls)))
    self.assertFalse(any(('DROP TABLE' in s for s in sqls)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_nullable_char_field_does_not_remake_or_raise(self):
    """
    Adding a nullable CharField should not remake the table and should
    not raise (ensures no erroneous attribute access like .one_to_one).
    """
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = CharField(max_length=50, null=True)
    new_field.set_attributes_from_name('nullable_char')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    sqls = [q['sql'] for q in ctx.captured_queries]
    self.assertFalse(any(('CREATE TABLE' in s for s in sqls)))
    self.assertFalse(any(('DROP TABLE' in s for s in sqls)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_nullable_binary_field_does_not_remake_or_raise(self):
    """
    Adding a nullable BinaryField should not remake the table and should
    not raise (regression guard).
    """
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = BinaryField(null=True, blank=True)
    new_field.set_attributes_from_name('nullable_binary')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    sqls = [q['sql'] for q in ctx.captured_queries]
    self.assertFalse(any(('CREATE TABLE' in s for s in sqls)))
    self.assertFalse(any(('DROP TABLE' in s for s in sqls)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_nullable_datetime_field_does_not_remake_or_raise(self):
    """
    Adding a nullable DateTimeField should not remake the table and should
    not raise (ensures safe attribute access).
    """
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = DateTimeField(null=True)
    new_field.set_attributes_from_name('nullable_datetime')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    sqls = [q['sql'] for q in ctx.captured_queries]
    self.assertFalse(any(('CREATE TABLE' in s for s in sqls)))
    self.assertFalse(any(('DROP TABLE' in s for s in sqls)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_primary_key_integer_field_remakes_table(self):
    """
    Adding a primary key field must remake the table (can't be done with
    ALTER TABLE ADD COLUMN). The gold patch ensures field.primary_key is
    considered; the candidate patch omits that check.
    """
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = IntegerField(primary_key=True)
    new_field.set_attributes_from_name('new_pk')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    sqls = [q['sql'] for q in ctx.captured_queries]
    self.assertTrue(any(('CREATE TABLE' in s for s in sqls)), sqls)

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_primary_key_autofield_remakes_table(self):
    """
    Adding an AutoField(primary_key=True) should also remake the table.
    """
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = AutoField(primary_key=True)
    new_field.set_attributes_from_name('auto_new_pk')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    sqls = [q['sql'] for q in ctx.captured_queries]
    self.assertTrue(any(('CREATE TABLE' in s for s in sqls)), sqls)

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_primary_key_bigint_field_remakes_table(self):
    """
    Adding a BigIntegerField(primary_key=True) forces a table remake.
    """
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = BigIntegerField(primary_key=True)
    new_field.set_attributes_from_name('bigint_new_pk')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    sqls = [q['sql'] for q in ctx.captured_queries]
    self.assertTrue(any(('CREATE TABLE' in s for s in sqls)), sqls)

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_primary_key_uuidfield_remakes_table(self):
    """
    Adding a UUIDField(primary_key=True) forces a table remake.
    """
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = UUIDField(primary_key=True)
    new_field.set_attributes_from_name('uuid_new_pk')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    sqls = [q['sql'] for q in ctx.captured_queries]
    self.assertTrue(any(('CREATE TABLE' in s for s in sqls)), sqls)

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_adding_nullable_field_does_not_access_one_to_one_attribute(self):
    """
    Regression guard: ensure adding a typical nullable field does not
    attempt to access a .one_to_one attribute (which would raise
    AttributeError in the candidate patch).
    The test verifies add_field completes successfully and does not
    remake the table.
    """
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = DecimalField(max_digits=5, decimal_places=2, null=True)
    new_field.set_attributes_from_name('nullable_decimal')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    sqls = [q['sql'] for q in ctx.captured_queries]
    self.assertFalse(any(('CREATE TABLE' in s for s in sqls)))
    self.assertFalse(any(('DROP TABLE' in s for s in sqls)))

import uuid
from django.db import connection
from django.db.models import AutoField, BigAutoField, IntegerField, CharField, UUIDField, SlugField, SmallAutoField, BigIntegerField, SmallIntegerField, PositiveIntegerField
import uuid
from django.db import connection
from django.db.models import AutoField, BigAutoField, IntegerField, CharField, UUIDField, SlugField, SmallAutoField, BigIntegerField, SmallIntegerField, PositiveIntegerField

def _make_test(name, FieldClass, kwargs=None):

    def test(self):
        self._add_primary_key_and_assert(FieldClass, field_kwargs=kwargs, name=name)
    return test
import types

def _attach_tests(SchemaTests):
    tests = [('add_primary_key_autofield', AutoField, None), ('add_primary_key_bigautofield', BigAutoField, None), ('add_primary_key_integerfield', IntegerField, None), ('add_primary_key_charfield', CharField, {'max_length': 50}), ('add_primary_key_uuidfield', UUIDField, {'default': uuid.uuid4}), ('add_primary_key_slugfield', SlugField, {'max_length': 50}), ('add_primary_key_smallautofield', SmallAutoField, None), ('add_primary_key_bigintegerfield', BigIntegerField, None), ('add_primary_key_smallintegerfield', SmallIntegerField, None), ('add_primary_key_positiveintegerfield', PositiveIntegerField, None)]
    for method_name, FieldClass, kwargs in tests:
        test_method = _make_test(method_name, FieldClass, kwargs)
        if not hasattr(SchemaTests, '_add_primary_key_and_assert'):
            setattr(SchemaTests, '_add_primary_key_and_assert', SchemaTests_AddPrimaryKeyFieldMixin._add_primary_key_and_assert)
        setattr(SchemaTests, 'test_%s' % method_name, test_method)
try:
    from .tests import SchemaTests
except Exception:
    SchemaTests = globals().get('SchemaTests')
if SchemaTests is not None:
    _attach_tests(SchemaTests)

@isolate_apps('schema')
@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_autofield_after_remove(self):

    class Foo(Model):
        name = CharField(max_length=30)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    self.isolated_local_models = [Foo]
    old_id = Foo._meta.get_field('id')
    with connection.schema_editor() as editor:
        editor.remove_field(Foo, old_id)
    new_pk = AutoField(primary_key=True)
    new_pk.set_attributes_from_name('new_id')
    with connection.schema_editor() as editor:
        editor.add_field(Foo, new_pk)
    self.assertEqual(self.get_primary_key(Foo._meta.db_table), 'new_id')

@isolate_apps('schema')
@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_integerfield_after_remove(self):

    class Bar(Model):
        title = CharField(max_length=50)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Bar)
    self.isolated_local_models = [Bar]
    old_id = Bar._meta.get_field('id')
    with connection.schema_editor() as editor:
        editor.remove_field(Bar, old_id)
    new_pk = IntegerField(primary_key=True)
    new_pk.set_attributes_from_name('pk_int')
    with connection.schema_editor() as editor:
        editor.add_field(Bar, new_pk)
    self.assertEqual(self.get_primary_key(Bar._meta.db_table), 'pk_int')

@isolate_apps('schema')
@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_bigautofield_after_remove(self):

    class Baz(Model):
        name = CharField(max_length=20)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Baz)
    self.isolated_local_models = [Baz]
    old_id = Baz._meta.get_field('id')
    with connection.schema_editor() as editor:
        editor.remove_field(Baz, old_id)
    new_pk = BigAutoField(primary_key=True)
    new_pk.set_attributes_from_name('big_id')
    with connection.schema_editor() as editor:
        editor.add_field(Baz, new_pk)
    self.assertEqual(self.get_primary_key(Baz._meta.db_table), 'big_id')

@isolate_apps('schema')
@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_smallautofield_after_remove(self):

    class Qux(Model):
        info = CharField(max_length=10)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Qux)
    self.isolated_local_models = [Qux]
    old_id = Qux._meta.get_field('id')
    with connection.schema_editor() as editor:
        editor.remove_field(Qux, old_id)
    new_pk = SmallAutoField(primary_key=True)
    new_pk.set_attributes_from_name('small_id')
    with connection.schema_editor() as editor:
        editor.add_field(Qux, new_pk)
    self.assertEqual(self.get_primary_key(Qux._meta.db_table), 'small_id')

@isolate_apps('schema')
@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_uuidfield_after_remove(self):

    class UuidModel(Model):
        name = CharField(max_length=10)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(UuidModel)
    self.isolated_local_models = [UuidModel]
    old_id = UuidModel._meta.get_field('id')
    with connection.schema_editor() as editor:
        editor.remove_field(UuidModel, old_id)
    new_pk = UUIDField(primary_key=True)
    new_pk.set_attributes_from_name('uuid_pk')
    with connection.schema_editor() as editor:
        editor.add_field(UuidModel, new_pk)
    self.assertEqual(self.get_primary_key(UuidModel._meta.db_table), 'uuid_pk')

@isolate_apps('schema')
@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_positiveinteger_after_remove(self):

    class PosIntModel(Model):
        data = CharField(max_length=10)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(PosIntModel)
    self.isolated_local_models = [PosIntModel]
    old_id = PosIntModel._meta.get_field('id')
    with connection.schema_editor() as editor:
        editor.remove_field(PosIntModel, old_id)
    new_pk = PositiveIntegerField(primary_key=True)
    new_pk.set_attributes_from_name('pos_pk')
    with connection.schema_editor() as editor:
        editor.add_field(PosIntModel, new_pk)
    self.assertEqual(self.get_primary_key(PosIntModel._meta.db_table), 'pos_pk')

@isolate_apps('schema')
@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_charfield_after_remove(self):

    class CharPKModel(Model):
        other = IntegerField()

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(CharPKModel)
    self.isolated_local_models = [CharPKModel]
    old_id = CharPKModel._meta.get_field('id')
    with connection.schema_editor() as editor:
        editor.remove_field(CharPKModel, old_id)
    new_pk = CharField(max_length=50, primary_key=True)
    new_pk.set_attributes_from_name('char_pk')
    with connection.schema_editor() as editor:
        editor.add_field(CharPKModel, new_pk)
    self.assertEqual(self.get_primary_key(CharPKModel._meta.db_table), 'char_pk')

@isolate_apps('schema')
@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_slugfield_after_remove(self):

    class SlugPKModel(Model):
        value = IntegerField()

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(SlugPKModel)
    self.isolated_local_models = [SlugPKModel]
    old_id = SlugPKModel._meta.get_field('id')
    with connection.schema_editor() as editor:
        editor.remove_field(SlugPKModel, old_id)
    new_pk = SlugField(primary_key=True)
    new_pk.set_attributes_from_name('slug_pk')
    with connection.schema_editor() as editor:
        editor.add_field(SlugPKModel, new_pk)
    self.assertEqual(self.get_primary_key(SlugPKModel._meta.db_table), 'slug_pk')

@isolate_apps('schema')
@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_biginteger_after_remove(self):

    class BigIntPKModel(Model):
        note = CharField(max_length=10)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(BigIntPKModel)
    self.isolated_local_models = [BigIntPKModel]
    old_id = BigIntPKModel._meta.get_field('id')
    with connection.schema_editor() as editor:
        editor.remove_field(BigIntPKModel, old_id)
    new_pk = BigIntegerField(primary_key=True)
    new_pk.set_attributes_from_name('bigint_pk')
    with connection.schema_editor() as editor:
        editor.add_field(BigIntPKModel, new_pk)
    self.assertEqual(self.get_primary_key(BigIntPKModel._meta.db_table), 'bigint_pk')

@isolate_apps('schema')
@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_various_types_consistency(self):

    class MixModel(Model):
        info = CharField(max_length=5)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(MixModel)
    self.isolated_local_models = [MixModel]
    old_id = MixModel._meta.get_field('id')
    with connection.schema_editor() as editor:
        editor.remove_field(MixModel, old_id)
    from django.db.models import DecimalField
    new_pk = DecimalField(max_digits=5, decimal_places=0, primary_key=True)
    new_pk.set_attributes_from_name('dec_pk')
    with connection.schema_editor() as editor:
        editor.add_field(MixModel, new_pk)
    self.assertEqual(self.get_primary_key(MixModel._meta.db_table), 'dec_pk')

import unittest
from django.db import connection
from django.db.transaction import atomic
from django.test import TransactionTestCase, skipUnlessDBFeature
from django.test.utils import CaptureQueriesContext
from django.db.models import AutoField, BigAutoField, IntegerField, CharField, SlugField, OneToOneField, ForeignKey, DateTimeField, UUIDField, DecimalField, CASCADE
from .models import Author, Note, Tag

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
class SQLiteAddFieldPrimaryKeyTests(TransactionTestCase):
    """
    Regression tests ensuring add_field remakes the table when adding a
    primary_key=True field on SQLite.
    """
    available_apps = []

    def test_add_field_primary_key_bigautofield(self):
        new_field = BigAutoField(primary_key=True)
        new_field.set_attributes_from_name('new_pk_big')
        self._assert_add_field_remakes_table(Author, new_field)

from django.test import TransactionTestCase
from django.db import connection
from django.db.models import AutoField, BigAutoField, IntegerField, CharField, SlugField, UUIDField, PositiveIntegerField
from .models import Author

class AddPrimaryKeyFieldTests(TransactionTestCase):
    """
    Tests for adding primary key fields to an existing table. These ensure
    that the table is remade so the new column becomes the primary key.
    """
    available_apps = []

    def _create_and_remove_id(self):
        with connection.schema_editor() as editor:
            editor.create_model(Author)
        with connection.schema_editor() as editor:
            editor.remove_field(Author, Author._meta.get_field('id'))

    def _cleanup(self):
        try:
            with connection.schema_editor() as editor:
                editor.delete_model(Author)
        except Exception:
            pass

from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from types import SimpleNamespace

def test_add_field_does_not_access_one_to_one_on_plain_field(self):
    """
    Plain fields without a one_to_one attribute should not cause
    AttributeError. The editor should call the base add_field path
    when the field is nullable and has no default/unique/primary key.
    """
    with connection.schema_editor() as editor:

        class PlainField:
            primary_key = False
            unique = False
            null = True
            many_to_many = False
            concrete = True
            column = 'plain'
        field = PlainField()
        base_add = mock.MagicMock()
        with mock.patch.object(BaseDatabaseSchemaEditor, 'add_field', new=base_add):
            editor.add_field(Author, field)
        base_add.assert_called_once()

def test_add_field_with_real_field_delegates_for_nullable_field(self):
    """
    Using a real IntegerField (nullable) should delegate to the base
    add_field (no table remake).
    """
    new_field = IntegerField(null=True)
    new_field.set_attributes_from_name('temp_int_field')
    with connection.schema_editor() as editor:
        base_add = mock.MagicMock()
        with mock.patch.object(BaseDatabaseSchemaEditor, 'add_field', new=base_add):
            editor.add_field(Author, new_field)
        base_add.assert_called_once()

def test_add_field_primary_key_triggers_remake(self):
    """
    A field declared primary_key=True must trigger a table remake.
    """

    class PKField:
        primary_key = True
        unique = False
        null = True
        many_to_many = False
        concrete = True
        column = 'pkcol'
    field = PKField()
    with connection.schema_editor() as editor:
        remake = mock.MagicMock()
        with mock.patch.object(type(editor), '_remake_table', new=remake):
            base_add = mock.MagicMock()
            with mock.patch.object(BaseDatabaseSchemaEditor, 'add_field', new=base_add):
                editor.add_field(Author, field)
        self.assertTrue(remake.called)
        base_add.assert_not_called()

def test_add_field_unique_triggers_remake(self):
    """
    A field with unique=True must trigger a table remake.
    """

    class UniqueField:
        primary_key = False
        unique = True
        null = True
        many_to_many = False
        concrete = True
        column = 'uniqcol'
    field = UniqueField()
    with connection.schema_editor() as editor:
        remake = mock.MagicMock()
        with mock.patch.object(type(editor), '_remake_table', new=remake):
            base_add = mock.MagicMock()
            with mock.patch.object(BaseDatabaseSchemaEditor, 'add_field', new=base_add):
                editor.add_field(Author, field)
        self.assertTrue(remake.called)
        base_add.assert_not_called()

def test_add_field_not_null_triggers_remake(self):
    """
    A NOT NULL field (null=False) must trigger a table remake.
    """

    class NotNullField:
        primary_key = False
        unique = False
        null = False
        many_to_many = False
        concrete = True
        column = 'notnull'
    field = NotNullField()
    with connection.schema_editor() as editor:
        remake = mock.MagicMock()
        with mock.patch.object(type(editor), '_remake_table', new=remake):
            base_add = mock.MagicMock()
            with mock.patch.object(BaseDatabaseSchemaEditor, 'add_field', new=base_add):
                editor.add_field(Author, field)
        self.assertTrue(remake.called)
        base_add.assert_not_called()

def test_add_field_effective_default_triggers_remake(self):
    """
    If effective_default(field) is not None, a table remake must occur.
    """

    class FieldWithDefault:
        primary_key = False
        unique = False
        null = True
        many_to_many = False
        concrete = True
        column = 'withdefault'
    field = FieldWithDefault()
    with connection.schema_editor() as editor:
        with mock.patch.object(type(editor), '_remake_table', new=mock.MagicMock()) as remake:
            base_add = mock.MagicMock()
            with mock.patch.object(BaseDatabaseSchemaEditor, 'add_field', new=base_add):
                with mock.patch.object(editor, 'effective_default', return_value='DEF'):
                    editor.add_field(Author, field)
        self.assertTrue(remake.called)
        base_add.assert_not_called()

def test_add_field_one_to_one_real_field_triggers_remake(self):
    """
    A OneToOneField addition should trigger a table remake because of the
    uniqueness and FK semantics.
    """
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    o2o_field = OneToOneField(Author, CASCADE, null=True)
    o2o_field.set_attributes_from_name('one_to_one_test')
    with connection.schema_editor() as editor:
        remake = mock.MagicMock()
        with mock.patch.object(type(editor), '_remake_table', new=remake):
            base_add = mock.MagicMock()
            with mock.patch.object(BaseDatabaseSchemaEditor, 'add_field', new=base_add):
                editor.add_field(Author, o2o_field)
        self.assertTrue(remake.called)
        base_add.assert_not_called()

def test_add_field_nullable_without_default_does_not_remake(self):
    """
    A nullable field without a default and no uniqueness/primary_key should
    delegate to the base implementation (no remake).
    """

    class SimpleNullable:
        primary_key = False
        unique = False
        null = True
        many_to_many = False
        concrete = True
        column = 'simpcol'
    field = SimpleNullable()
    with connection.schema_editor() as editor:
        base_add = mock.MagicMock()
        with mock.patch.object(BaseDatabaseSchemaEditor, 'add_field', new=base_add):
            remake = mock.MagicMock()
            with mock.patch.object(type(editor), '_remake_table', new=remake):
                editor.add_field(Author, field)
        base_add.assert_called_once()
        self.assertFalse(remake.called)

def test_add_field_missing_one_to_one_attribute_on_real_field_does_not_raise(self):
    """
    Ensure adding a regular field (which may not expose a one_to_one attribute)
    does not raise an AttributeError. This guards against candidate patches that
    naively access .one_to_one on all fields.
    """
    new_field = CharField(max_length=10, null=True)
    new_field.set_attributes_from_name('check_no_one_to_one')
    with connection.schema_editor() as editor:
        base_add = mock.MagicMock()
        with mock.patch.object(BaseDatabaseSchemaEditor, 'add_field', new=base_add):
            editor.add_field(Author, new_field)
        base_add.assert_called_once()