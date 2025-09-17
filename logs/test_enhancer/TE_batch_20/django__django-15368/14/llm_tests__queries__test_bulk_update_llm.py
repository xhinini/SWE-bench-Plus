from importlib import import_module
import sys
from django.test import SimpleTestCase
from importlib import import_module
import sys
from django.test import SimpleTestCase

class ExpressionImportRemovalTests(SimpleTestCase):

    def setUp(self):
        if 'django.db.models.query' in sys.modules:
            del sys.modules['django.db.models.query']
        self.mod = import_module('django.db.models.query')

    def test_no_attribute_via_getattr(self):
        self.assertIsNone(getattr(self.mod, 'Expression', None))

    def test_attribute_access_raises_attribute_error(self):
        with self.assertRaises(AttributeError):
            _ = self.mod.Expression

    def test_name_not_in_dir(self):
        self.assertNotIn('Expression', dir(self.mod))

    def test_from_import_raises_import_error(self):
        with self.assertRaises(ImportError):
            exec('from django.db.models.query import Expression')

    def test_importlib_attribute_missing(self):
        mod = import_module('django.db.models.query')
        self.assertFalse(hasattr(mod, 'Expression'))

    def test_module_dict_has_no_expression_key(self):
        self.assertNotIn('Expression', self.mod.__dict__)

    def test_attrs_do_not_contain_expression(self):
        names = [name for name in self.mod.__dict__.keys() if 'Expression' in name]
        self.assertEqual(names, [])

    def test_getattr_without_default_raises(self):
        with self.assertRaises(AttributeError):
            getattr(self.mod, 'Expression')

    def test_from_import_in_local_namespace_fails(self):
        ns = {}
        with self.assertRaises(ImportError):
            exec('from django.db.models.query import Expression', ns)