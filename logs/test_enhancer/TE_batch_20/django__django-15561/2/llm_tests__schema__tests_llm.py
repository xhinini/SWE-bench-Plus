import unittest
from django.db import models
from django.db.models import CharField, Field

class FieldNonDBAttrsTests(unittest.TestCase):

    def test_non_db_attrs_exists_on_field(self):
        self.assertTrue(hasattr(Field, 'non_db_attrs'))

    def test_non_db_attrs_is_tuple(self):
        non_db = getattr(Field, 'non_db_attrs')
        self.assertIsInstance(non_db, tuple)

    def test_non_db_attrs_contains_choices(self):
        non_db = getattr(Field, 'non_db_attrs')
        self.assertIn('choices', non_db)

    def test_non_db_attrs_contains_db_column(self):
        non_db = getattr(Field, 'non_db_attrs')
        self.assertIn('db_column', non_db)

    def test_non_db_attrs_contains_validators(self):
        non_db = getattr(Field, 'non_db_attrs')
        self.assertIn('validators', non_db)

    def test_non_db_attrs_contains_verbose_name(self):
        non_db = getattr(Field, 'non_db_attrs')
        self.assertIn('verbose_name', non_db)

    def test_non_db_attrs_contains_on_delete(self):
        non_db = getattr(Field, 'non_db_attrs')
        self.assertIn('on_delete', non_db)

    def test_non_db_attrs_inherited_by_subclass(self):
        self.assertTrue(hasattr(CharField, 'non_db_attrs'))
        self.assertEqual(getattr(CharField, 'non_db_attrs'), getattr(Field, 'non_db_attrs'))

    def test_non_db_attrs_expected_contents(self):
        non_db = set(getattr(Field, 'non_db_attrs'))
        expected = {'blank', 'choices', 'db_column', 'editable', 'error_messages', 'help_text', 'limit_choices_to', 'on_delete', 'related_name', 'related_query_name', 'validators', 'verbose_name'}
        self.assertTrue(expected.issubset(non_db))