from django.test import SimpleTestCase
from django.db.migrations.state import ProjectState
import types

class RealAppsInitTests(SimpleTestCase):

    def test_real_apps_rejects_list_without_message(self):
        with self.assertRaises(AssertionError) as cm:
            ProjectState(real_apps=['contenttypes'])
        self.assertEqual(cm.exception.args, ())

    def test_real_apps_rejects_empty_list_without_message(self):
        with self.assertRaises(AssertionError) as cm:
            ProjectState(real_apps=[])
        self.assertEqual(cm.exception.args, ())

    def test_real_apps_rejects_tuple_without_message(self):
        with self.assertRaises(AssertionError) as cm:
            ProjectState(real_apps=('contenttypes',))
        self.assertEqual(cm.exception.args, ())

    def test_real_apps_rejects_empty_tuple_without_message(self):
        with self.assertRaises(AssertionError) as cm:
            ProjectState(real_apps=())
        self.assertEqual(cm.exception.args, ())

    def test_real_apps_rejects_generator_without_message(self):
        gen = (x for x in ('contenttypes',))
        with self.assertRaises(AssertionError) as cm:
            ProjectState(real_apps=gen)
        self.assertEqual(cm.exception.args, ())

    def test_real_apps_rejects_frozenset_without_message(self):
        with self.assertRaises(AssertionError) as cm:
            ProjectState(real_apps=frozenset({'contenttypes'}))
        self.assertEqual(cm.exception.args, ())

    def test_real_apps_rejects_string_without_message(self):
        with self.assertRaises(AssertionError) as cm:
            ProjectState(real_apps='contenttypes')
        self.assertEqual(cm.exception.args, ())

    def test_real_apps_rejects_range_without_message(self):
        with self.assertRaises(AssertionError) as cm:
            ProjectState(real_apps=range(1))
        self.assertEqual(cm.exception.args, ())