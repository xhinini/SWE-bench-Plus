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