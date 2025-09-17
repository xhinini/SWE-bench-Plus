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

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_autofield_triggers_remake(self):
    """Adding an AutoField(primary_key=True) must remake the table on SQLite."""
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = AutoField(primary_key=True)
    new_field.set_attributes_from_name('new_id')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_integerfield_triggers_remake(self):
    """Adding an IntegerField(primary_key=True) must remake the table on SQLite."""
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = IntegerField(primary_key=True)
    new_field.set_attributes_from_name('new_pk_int')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_bigautofield_triggers_remake(self):
    """Adding a BigAutoField(primary_key=True) must remake the table on SQLite."""
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = BigAutoField(primary_key=True)
    new_field.set_attributes_from_name('new_big_id')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_smallautofield_triggers_remake(self):
    """Adding a SmallAutoField(primary_key=True) must remake the table on SQLite."""
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = SmallAutoField(primary_key=True)
    new_field.set_attributes_from_name('new_small_id')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_uuidfield_triggers_remake(self):
    """Adding a UUIDField(primary_key=True) must remake the table on SQLite."""
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = UUIDField(primary_key=True)
    new_field.set_attributes_from_name('new_uuid')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_onetoonefield_triggers_remake(self):
    """Adding a OneToOneField(primary_key=True) must remake the table on SQLite."""
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = OneToOneField(Author, CASCADE, primary_key=True, null=True)
    new_field.set_attributes_from_name('o2o_pk')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_fk_triggers_remake(self):
    """Adding a ForeignKey(primary_key=True) must remake the table on SQLite."""
    with connection.schema_editor() as editor:
        editor.create_model(Author)
        editor.create_model(Book)
    new_field = ForeignKey(Author, CASCADE, primary_key=True, null=True)
    new_field.set_attributes_from_name('fk_pk')
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Book, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_preserves_data(self):
    """
    Adding a primary key field via a table remake should preserve existing data.
    This ensures the remake path is actually taken and correctly copies rows.
    """
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    Author.objects.create(name='A1')
    Author.objects.create(name='A2')
    new_field = IntegerField(primary_key=True)
    new_field.set_attributes_from_name('new_pk_preserve')
    with connection.schema_editor() as editor:
        with CaptureQueriesContext(connection) as ctx:
            editor.add_field(Author, new_field)
        self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))
    self.assertEqual(Author.objects.count(), 2)

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_clears_deferred_sql(self):
    """
    Ensure that after remaking the table to add a primary key field, no
    leftover deferred SQL references remain for the added table.
    """
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = AutoField(primary_key=True)
    new_field.set_attributes_from_name('new_id_cleanup')
    with connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
        for stmt in list(editor.deferred_sql):
            if isinstance(stmt, Statement):
                self.assertFalse(stmt.references_table(Author._meta.db_table))

import unittest
from django.db import connection
from django.db.models import IntegerField, CharField, BooleanField, BinaryField, FloatField, DecimalField, DateField, DateTimeField, AutoField, TextField
from django.test import TransactionTestCase
from django.test.utils import CaptureQueriesContext
from .models import Author

class AddFieldRegressionTests(TransactionTestCase):
    """
    Regression tests for sqlite3.schema.DatabaseSchemaEditor.add_field

    These tests ensure adding simple nullable fields doesn't raise
    AttributeError (due to accessing field.one_to_one) and that adding a
    new primary-key field triggers a table remake (CREATE TABLE).
    """
    available_apps = []

    def _create_author_table(self):
        with connection.schema_editor() as editor:
            editor.create_model(Author)

from django.db.backends.sqlite3 import schema as sqlite_schema

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_integer_calls_remake(self):
    new_field = IntegerField(primary_key=True)
    new_field.set_attributes_from_name('new_pk_int')
    with mock.patch.object(sqlite_schema.DatabaseSchemaEditor, '_remake_table') as mocked:
        with connection.schema_editor() as editor:
            editor.add_field(Author, new_field)
    self.assertTrue(mocked.called)
    called_args, called_kwargs = mocked.call_args
    self.assertIs(called_args[0], Author)
    self.assertIn('create_field', called_kwargs)
    self.assertIs(called_kwargs['create_field'], new_field)

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_char_calls_remake(self):
    new_field = CharField(max_length=10, primary_key=True)
    new_field.set_attributes_from_name('new_pk_char')
    with mock.patch.object(sqlite_schema.DatabaseSchemaEditor, '_remake_table') as mocked:
        with connection.schema_editor() as editor:
            editor.add_field(Author, new_field)
    self.assertTrue(mocked.called)
    called_args, called_kwargs = mocked.call_args
    self.assertIs(called_args[0], Author)
    self.assertIs(called_kwargs['create_field'], new_field)

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_bigautofield_calls_remake(self):
    new_field = BigAutoField(primary_key=True)
    new_field.set_attributes_from_name('new_pk_bigauto')
    with mock.patch.object(sqlite_schema.DatabaseSchemaEditor, '_remake_table') as mocked:
        with connection.schema_editor() as editor:
            editor.add_field(Author, new_field)
    self.assertTrue(mocked.called)
    called_args, called_kwargs = mocked.call_args
    self.assertIs(called_args[0], Author)
    self.assertIs(called_kwargs['create_field'], new_field)

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_uuid_calls_remake(self):
    new_field = UUIDField(primary_key=True)
    new_field.set_attributes_from_name('new_pk_uuid')
    with mock.patch.object(sqlite_schema.DatabaseSchemaEditor, '_remake_table') as mocked:
        with connection.schema_editor() as editor:
            editor.add_field(Author, new_field)
    self.assertTrue(mocked.called)
    called_args, called_kwargs = mocked.call_args
    self.assertIs(called_args[0], Author)
    self.assertIs(called_kwargs['create_field'], new_field)

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_slug_calls_remake(self):
    new_field = SlugField(primary_key=True)
    new_field.set_attributes_from_name('new_pk_slug')
    with mock.patch.object(sqlite_schema.DatabaseSchemaEditor, '_remake_table') as mocked:
        with connection.schema_editor() as editor:
            editor.add_field(Author, new_field)
    self.assertTrue(mocked.called)
    called_args, called_kwargs = mocked.call_args
    self.assertIs(called_args[0], Author)
    self.assertIs(called_kwargs['create_field'], new_field)

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_smallautofield_calls_remake(self):
    new_field = SmallAutoField(primary_key=True)
    new_field.set_attributes_from_name('new_pk_smallauto')
    with mock.patch.object(sqlite_schema.DatabaseSchemaEditor, '_remake_table') as mocked:
        with connection.schema_editor() as editor:
            editor.add_field(Author, new_field)
    self.assertTrue(mocked.called)
    called_args, called_kwargs = mocked.call_args
    self.assertIs(called_args[0], Author)
    self.assertIs(called_kwargs['create_field'], new_field)

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_one_to_one_calls_remake(self):
    new_field = OneToOneField(Author, CASCADE, primary_key=True, null=True)
    new_field.set_attributes_from_name('new_pk_o2o')
    with mock.patch.object(sqlite_schema.DatabaseSchemaEditor, '_remake_table') as mocked:
        with connection.schema_editor() as editor:
            editor.add_field(Author, new_field)
    self.assertTrue(mocked.called)
    called_args, called_kwargs = mocked.call_args
    self.assertIs(called_args[0], Author)
    self.assertIs(called_kwargs['create_field'], new_field)

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_big_integer_calls_remake(self):
    new_field = BigIntegerField(primary_key=True)
    new_field.set_attributes_from_name('new_pk_bigint')
    with mock.patch.object(sqlite_schema.DatabaseSchemaEditor, '_remake_table') as mocked:
        with connection.schema_editor() as editor:
            editor.add_field(Author, new_field)
    self.assertTrue(mocked.called)
    called_args, called_kwargs = mocked.call_args
    self.assertIs(called_args[0], Author)
    self.assertIs(called_kwargs['create_field'], new_field)

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_binaryfield_calls_remake(self):
    new_field = BinaryField(primary_key=True)
    new_field.set_attributes_from_name('new_pk_binary')
    with mock.patch.object(sqlite_schema.DatabaseSchemaEditor, '_remake_table') as mocked:
        with connection.schema_editor() as editor:
            editor.add_field(Author, new_field)
    self.assertTrue(mocked.called)
    called_args, called_kwargs = mocked.call_args
    self.assertIs(called_args[0], Author)
    self.assertIs(called_kwargs['create_field'], new_field)

from types import SimpleNamespace

def test_add_field_triggers_remake_for_primary_key_integerfield(self):
    with connection.schema_editor() as editor:
        model = SimpleNamespace(_meta=SimpleNamespace(db_table='fake_table', local_concrete_fields=[]))
        field = IntegerField()
        field.set_attributes_from_name('new_pk_int')
        field.primary_key = True
        with mock.patch.object(editor, '_remake_table') as mock_rm:
            editor.add_field(model, field)
        mock_rm.assert_called_once_with(model, create_field=field)

def test_add_field_triggers_remake_for_primary_key_autofield(self):
    with connection.schema_editor() as editor:
        model = SimpleNamespace(_meta=SimpleNamespace(db_table='fake_table2', local_concrete_fields=[]))
        field = AutoField()
        field.set_attributes_from_name('new_pk_auto')
        field.primary_key = True
        with mock.patch.object(editor, '_remake_table') as mock_rm:
            editor.add_field(model, field)
        mock_rm.assert_called_once_with(model, create_field=field)

def test_add_field_triggers_remake_for_primary_key_bigautofield(self):
    with connection.schema_editor() as editor:
        model = SimpleNamespace(_meta=SimpleNamespace(db_table='fake_table3', local_concrete_fields=[]))
        field = BigAutoField()
        field.set_attributes_from_name('new_pk_bigauto')
        field.primary_key = True
        with mock.patch.object(editor, '_remake_table') as mock_rm:
            editor.add_field(model, field)
        mock_rm.assert_called_once_with(model, create_field=field)

def test_add_field_triggers_remake_for_primary_key_smallautofield(self):
    with connection.schema_editor() as editor:
        model = SimpleNamespace(_meta=SimpleNamespace(db_table='fake_table4', local_concrete_fields=[]))
        field = SmallAutoField()
        field.set_attributes_from_name('new_pk_smallauto')
        field.primary_key = True
        with mock.patch.object(editor, '_remake_table') as mock_rm:
            editor.add_field(model, field)
        mock_rm.assert_called_once_with(model, create_field=field)

def test_add_field_triggers_remake_for_primary_key_bigintegerfield(self):
    with connection.schema_editor() as editor:
        model = SimpleNamespace(_meta=SimpleNamespace(db_table='fake_table5', local_concrete_fields=[]))
        field = BigIntegerField()
        field.set_attributes_from_name('new_pk_bigint')
        field.primary_key = True
        with mock.patch.object(editor, '_remake_table') as mock_rm:
            editor.add_field(model, field)
        mock_rm.assert_called_once_with(model, create_field=field)

def test_add_field_triggers_remake_for_primary_key_smallintegerfield(self):
    with connection.schema_editor() as editor:
        model = SimpleNamespace(_meta=SimpleNamespace(db_table='fake_table6', local_concrete_fields=[]))
        field = SmallIntegerField()
        field.set_attributes_from_name('new_pk_smallint')
        field.primary_key = True
        with mock.patch.object(editor, '_remake_table') as mock_rm:
            editor.add_field(model, field)
        mock_rm.assert_called_once_with(model, create_field=field)

def test_add_field_triggers_remake_for_primary_key_uuidfield(self):
    with connection.schema_editor() as editor:
        model = SimpleNamespace(_meta=SimpleNamespace(db_table='fake_table7', local_concrete_fields=[]))
        field = UUIDField()
        field.set_attributes_from_name('new_pk_uuid')
        field.primary_key = True
        with mock.patch.object(editor, '_remake_table') as mock_rm:
            editor.add_field(model, field)
        mock_rm.assert_called_once_with(model, create_field=field)

def test_add_field_triggers_remake_for_primary_key_charfield(self):
    with connection.schema_editor() as editor:
        model = SimpleNamespace(_meta=SimpleNamespace(db_table='fake_table8', local_concrete_fields=[]))
        field = CharField(max_length=30)
        field.set_attributes_from_name('new_pk_char')
        field.primary_key = True
        with mock.patch.object(editor, '_remake_table') as mock_rm:
            editor.add_field(model, field)
        mock_rm.assert_called_once_with(model, create_field=field)

def test_add_field_triggers_remake_for_primary_key_slugfield(self):
    with connection.schema_editor() as editor:
        model = SimpleNamespace(_meta=SimpleNamespace(db_table='fake_table9', local_concrete_fields=[]))
        field = SlugField()
        field.set_attributes_from_name('new_pk_slug')
        field.primary_key = True
        with mock.patch.object(editor, '_remake_table') as mock_rm:
            editor.add_field(model, field)
        mock_rm.assert_called_once_with(model, create_field=field)

def test_add_field_triggers_remake_for_primary_key_positiveintegerfield(self):
    with connection.schema_editor() as editor:
        model = SimpleNamespace(_meta=SimpleNamespace(db_table='fake_table10', local_concrete_fields=[]))
        field = PositiveIntegerField()
        field.set_attributes_from_name('new_pk_posint')
        field.primary_key = True
        with mock.patch.object(editor, '_remake_table') as mock_rm:
            editor.add_field(model, field)
        mock_rm.assert_called_once_with(model, create_field=field)

import unittest
from django.test.utils import isolate_apps
from django.db import connection
from django.test.utils import CaptureQueriesContext

@isolate_apps('schema')
@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_charfield_remakes_table(self):

    class Foo(models.Model):
        name = CharField(max_length=50)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    with connection.schema_editor() as editor:
        editor.remove_field(Foo, Foo._meta.get_field('id'))
    new_field = CharField(max_length=10, primary_key=True)
    new_field.set_attributes_from_name('pkcol')
    new_field.model = Foo
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Foo, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'].upper() for q in ctx.captured_queries)))
    self.assertEqual(self.get_primary_key(Foo._meta.db_table), 'pkcol')

@isolate_apps('schema')
@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_slugfield_remakes_table(self):

    class Foo(models.Model):
        name = CharField(max_length=50)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    with connection.schema_editor() as editor:
        editor.remove_field(Foo, Foo._meta.get_field('id'))
    new_field = SlugField(max_length=30, primary_key=True)
    new_field.set_attributes_from_name('pkslug')
    new_field.model = Foo
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Foo, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'].upper() for q in ctx.captured_queries)))
    self.assertEqual(self.get_primary_key(Foo._meta.db_table), 'pkslug')

@isolate_apps('schema')
@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_integerfield_remakes_table(self):

    class Foo(models.Model):
        name = CharField(max_length=50)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    with connection.schema_editor() as editor:
        editor.remove_field(Foo, Foo._meta.get_field('id'))
    new_field = IntegerField(primary_key=True)
    new_field.set_attributes_from_name('pkint')
    new_field.model = Foo
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Foo, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'].upper() for q in ctx.captured_queries)))
    self.assertEqual(self.get_primary_key(Foo._meta.db_table), 'pkint')

@isolate_apps('schema')
@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_autofield_remakes_table(self):

    class Foo(models.Model):
        name = CharField(max_length=50)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    with connection.schema_editor() as editor:
        editor.remove_field(Foo, Foo._meta.get_field('id'))
    new_field = AutoField(primary_key=True)
    new_field.set_attributes_from_name('pkauto')
    new_field.model = Foo
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Foo, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'].upper() for q in ctx.captured_queries)))
    self.assertEqual(self.get_primary_key(Foo._meta.db_table), 'pkauto')

@isolate_apps('schema')
@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_bigautofield_remakes_table(self):

    class Foo(models.Model):
        name = CharField(max_length=50)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    with connection.schema_editor() as editor:
        editor.remove_field(Foo, Foo._meta.get_field('id'))
    new_field = BigAutoField(primary_key=True)
    new_field.set_attributes_from_name('pkbigauto')
    new_field.model = Foo
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Foo, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'].upper() for q in ctx.captured_queries)))
    self.assertEqual(self.get_primary_key(Foo._meta.db_table), 'pkbigauto')

@isolate_apps('schema')
@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_smallautofield_remakes_table(self):

    class Foo(models.Model):
        name = CharField(max_length=50)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    with connection.schema_editor() as editor:
        editor.remove_field(Foo, Foo._meta.get_field('id'))
    new_field = SmallAutoField(primary_key=True)
    new_field.set_attributes_from_name('pksmallauto')
    new_field.model = Foo
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Foo, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'].upper() for q in ctx.captured_queries)))
    self.assertEqual(self.get_primary_key(Foo._meta.db_table), 'pksmallauto')

@isolate_apps('schema')
@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_uuidfield_remakes_table(self):

    class Foo(models.Model):
        name = CharField(max_length=50)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    with connection.schema_editor() as editor:
        editor.remove_field(Foo, Foo._meta.get_field('id'))
    new_field = UUIDField(primary_key=True)
    new_field.set_attributes_from_name('pkuuid')
    new_field.model = Foo
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Foo, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'].upper() for q in ctx.captured_queries)))
    self.assertEqual(self.get_primary_key(Foo._meta.db_table), 'pkuuid')

@isolate_apps('schema')
@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_bigintegerfield_remakes_table(self):

    class Foo(models.Model):
        name = CharField(max_length=50)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    with connection.schema_editor() as editor:
        editor.remove_field(Foo, Foo._meta.get_field('id'))
    new_field = BigIntegerField(primary_key=True)
    new_field.set_attributes_from_name('pkbigint')
    new_field.model = Foo
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Foo, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'].upper() for q in ctx.captured_queries)))
    self.assertEqual(self.get_primary_key(Foo._meta.db_table), 'pkbigint')

@isolate_apps('schema')
@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_field_primary_key_smallintegerfield_remakes_table(self):

    class Foo(models.Model):
        name = CharField(max_length=50)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    with connection.schema_editor() as editor:
        editor.remove_field(Foo, Foo._meta.get_field('id'))
    new_field = SmallIntegerField(primary_key=True)
    new_field.set_attributes_from_name('pksmallint')
    new_field.model = Foo
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Foo, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'].upper() for q in ctx.captured_queries)))
    self.assertEqual(self.get_primary_key(Foo._meta.db_table), 'pksmallint')

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_integerfield_primary_key_remakes_table(self):
    """
    Adding an IntegerField(primary_key=True) must remake the table on SQLite.
    """
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = IntegerField(primary_key=True)
    new_field.set_attributes_from_name('new_pk')
    new_field.model = Author
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))
    self.assertEqual(self.get_primary_key(Author._meta.db_table), 'new_pk')

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_autofield_primary_key_remakes_table(self):
    """
    Adding an AutoField(primary_key=True) must remake the table on SQLite.
    """
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = AutoField(primary_key=True)
    new_field.set_attributes_from_name('auto_pk')
    new_field.model = Author
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))
    self.assertEqual(self.get_primary_key(Author._meta.db_table), 'auto_pk')

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_bigautofield_primary_key_remakes_table(self):
    """
    Adding a BigAutoField(primary_key=True) must remake the table on SQLite.
    """
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = BigAutoField(primary_key=True)
    new_field.set_attributes_from_name('big_pk')
    new_field.model = Author
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))
    self.assertEqual(self.get_primary_key(Author._meta.db_table), 'big_pk')

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_smallautofield_primary_key_remakes_table(self):
    """
    Adding a SmallAutoField(primary_key=True) must remake the table on SQLite.
    """
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = SmallAutoField(primary_key=True)
    new_field.set_attributes_from_name('small_pk')
    new_field.model = Author
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))
    self.assertEqual(self.get_primary_key(Author._meta.db_table), 'small_pk')

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_charfield_primary_key_remakes_table(self):
    """
    Adding a CharField(primary_key=True) must remake the table on SQLite.
    """
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = CharField(max_length=50, primary_key=True)
    new_field.set_attributes_from_name('char_pk')
    new_field.model = Author
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))
    self.assertEqual(self.get_primary_key(Author._meta.db_table), 'char_pk')

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_primary_key_updates_foreign_key_references(self):
    """
    Adding a primary key to a referenced table should remake the table and
    preserve/update foreign key references from another table.
    """
    with connection.schema_editor() as editor:
        editor.create_model(Author)
        editor.create_model(Book)
    self.assertForeignKeyExists(Book, 'author_id', 'schema_author')
    new_field = IntegerField(primary_key=True)
    new_field.set_attributes_from_name('new_pk')
    new_field.model = Author
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))
    self.assertForeignKeyExists(Book, 'author_id', 'schema_author')
    self.assertEqual(self.get_primary_key(Author._meta.db_table), 'new_pk')

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_integer_pk_without_default_does_remake(self):
    """
    Even when the new primary key field has no explicit default, a remake must
    be performed (so existing rows are handled by the table rebuild logic).
    """
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    Author.objects.create(name='X')
    new_field = IntegerField(primary_key=True)
    new_field.set_attributes_from_name('new_pk2')
    new_field.model = Author
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))
    self.assertEqual(self.get_primary_key(Author._meta.db_table), 'new_pk2')

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_autofield_pk_with_existing_rows_remakes_table(self):
    """
    Adding an AutoField primary key to a table with existing rows must remake
    the table so that the new PK column is correctly created/handled.
    """
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    Author.objects.create(name='A')
    Author.objects.create(name='B')
    new_field = AutoField(primary_key=True)
    new_field.set_attributes_from_name('auto_pk2')
    new_field.model = Author
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))
    self.assertEqual(self.get_primary_key(Author._meta.db_table), 'auto_pk2')

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_char_pk_preserves_uniques_and_indexes(self):
    """
    Adding a CharField(primary_key=True) must remake the table and preserve
    other constraints (the important part is that a remake occurs).
    """
    with connection.schema_editor() as editor:
        editor.create_model(Tag)
    Tag.objects.create(title='t', slug='s')
    new_field = CharField(max_length=32, primary_key=True)
    new_field.set_attributes_from_name('slug_pk')
    new_field.model = Tag
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Tag, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))
    self.assertEqual(self.get_primary_key(Tag._meta.db_table), 'slug_pk')

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_nullable_integer_field_sqlite(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = IntegerField(null=True)
    new_field.set_attributes_from_name('nullable_int')
    with connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    columns = self.column_classes(Author)
    self.assertIn('nullable_int', columns)
    self.assertTrue(columns['nullable_int'][1][6])

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_nullable_charfield_sqlite(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = CharField(max_length=50, null=True)
    new_field.set_attributes_from_name('nullable_char')
    with connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    columns = self.column_classes(Author)
    self.assertIn('nullable_char', columns)
    self.assertTrue(columns['nullable_char'][1][6])

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_nullable_textfield_sqlite(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = TextField(null=True)
    new_field.set_attributes_from_name('nullable_text')
    with connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    columns = self.column_classes(Author)
    self.assertIn('nullable_text', columns)
    self.assertTrue(columns['nullable_text'][1][6])

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_nullable_binaryfield_sqlite(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = BinaryField(null=True, blank=True)
    new_field.set_attributes_from_name('nullable_bits')
    with connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    columns = self.column_classes(Author)
    self.assertIn('nullable_bits', columns)
    self.assertTrue(columns['nullable_bits'][1][6])

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_nullable_datetimefield_sqlite(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = DateTimeField(null=True)
    new_field.set_attributes_from_name('nullable_dt')
    with connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    columns = self.column_classes(Author)
    self.assertIn('nullable_dt', columns)
    self.assertTrue(columns['nullable_dt'][1][6])

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_nullable_booleanfield_sqlite(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = BooleanField(null=True)
    new_field.set_attributes_from_name('nullable_bool')
    with connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    columns = self.column_classes(Author)
    self.assertIn('nullable_bool', columns)
    self.assertTrue(columns['nullable_bool'][1][6])

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_nullable_floatfield_sqlite(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = FloatField(null=True)
    new_field.set_attributes_from_name('nullable_float')
    with connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    columns = self.column_classes(Author)
    self.assertIn('nullable_float', columns)
    self.assertTrue(columns['nullable_float'][1][6])

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_primary_key_field_rebuilds_table_sqlite(self):
    """
    Adding a new primary key field should trigger a table remake on SQLite,
    not an ALTER TABLE ADD COLUMN. After adding, the primary key should be
    the new column.
    """
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = IntegerField(primary_key=True)
    new_field.set_attributes_from_name('new_pk')
    with connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    pk_col = self.get_primary_key(Author._meta.db_table)
    self.assertEqual(pk_col, 'new_pk')

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_unique_field_rebuilds_table_sqlite(self):
    """
    Adding a unique field should rebuild the table so the unique constraint
    exists afterwards.
    """
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    new_field = CharField(max_length=30, unique=True)
    new_field.set_attributes_from_name('unique_col')
    with connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    uniques = self.get_uniques(Author._meta.db_table)
    self.assertIn('unique_col', uniques)

@unittest.skipUnless(connection.vendor == 'sqlite', 'SQLite specific')
def test_add_o2o_field_nullable_sqlite(self):
    """
    Adding a OneToOneField (nullable) should succeed (regression for
    touching a potentially non-existing attribute on Field).
    """
    with connection.schema_editor() as editor:
        editor.create_model(Author)
        editor.create_model(Note)
    new_field = OneToOneField(Note, CASCADE, null=True)
    new_field.set_attributes_from_name('o2o_note')
    with connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    columns = self.column_classes(Author)
    self.assertIn('o2o_note_id', columns)
    self.assertTrue(columns['o2o_note_id'][1][6])

def _assert_add_primary_key_remakes_table(self, field):
    """
    Helper to remove the existing implicit id column, add `field` as a new
    primary key, and assert that the schema editor remade the table
    (observed via CREATE TABLE in the captured queries) and that the
    database primary key is the newly added column.
    """
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    with connection.schema_editor() as editor:
        editor.remove_field(Author, Author._meta.get_field('id'))
    field.set_attributes_from_name('newpk')
    field.model = Author
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))
    self.assertEqual(self.get_primary_key(Author._meta.db_table), 'newpk')

def test_add_primary_key_integerfield_remakes_table(self):
    self._assert_add_primary_key_remakes_table(IntegerField(primary_key=True))

def test_add_primary_key_autofield_remakes_table(self):
    self._assert_add_primary_key_remakes_table(AutoField(primary_key=True))

def test_add_primary_key_bigautofield_remakes_table(self):
    self._assert_add_primary_key_remakes_table(BigAutoField(primary_key=True))

def test_add_primary_key_smallautofield_remakes_table(self):
    self._assert_add_primary_key_remakes_table(SmallAutoField(primary_key=True))

def test_add_primary_key_charfield_remakes_table(self):
    self._assert_add_primary_key_remakes_table(CharField(max_length=50, primary_key=True))

def test_add_primary_key_slugfield_remakes_table(self):
    self._assert_add_primary_key_remakes_table(SlugField(primary_key=True))

def test_add_primary_key_uuidfield_remakes_table(self):
    self._assert_add_primary_key_remakes_table(UUIDField(primary_key=True))

def test_add_primary_key_bigintegerfield_remakes_table(self):
    self._assert_add_primary_key_remakes_table(BigIntegerField(primary_key=True))

def test_add_primary_key_charfield_non_null_remakes_table(self):
    self._assert_add_primary_key_remakes_table(CharField(max_length=30, primary_key=True, null=False))

def test_add_primary_key_after_removal_sets_pk(self):
    """
    Slightly different shape: ensure after removing the implicit id, adding
    an AutoField primary key both remakes the table and sets the PK.
    """
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    with connection.schema_editor() as editor:
        editor.remove_field(Author, Author._meta.get_field('id'))
    new_field = AutoField(primary_key=True)
    new_field.set_attributes_from_name('newpk')
    new_field.model = Author
    with CaptureQueriesContext(connection) as ctx, connection.schema_editor() as editor:
        editor.add_field(Author, new_field)
    self.assertTrue(any(('CREATE TABLE' in q['sql'] for q in ctx.captured_queries)))
    self.assertEqual(self.get_primary_key(Author._meta.db_table), 'newpk')