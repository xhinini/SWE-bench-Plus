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

from django.test import SimpleTestCase
from django.db.migrations.state import ProjectState

class ProjectStateRealAppsMessageTests(SimpleTestCase):

    def test_real_apps_list_has_empty_assertion_message(self):
        self._assert_assertion_message_empty(['contenttypes'])

    def test_real_apps_tuple_has_empty_assertion_message(self):
        self._assert_assertion_message_empty(('contenttypes',))

    def test_real_apps_frozenset_has_empty_assertion_message(self):
        self._assert_assertion_message_empty(frozenset({'contenttypes'}))

    def test_real_apps_generator_has_empty_assertion_message(self):
        self._assert_assertion_message_empty((x for x in ['contenttypes']))

    def test_real_apps_map_has_empty_assertion_message(self):
        self._assert_assertion_message_empty(map(lambda x: x, ['contenttypes']))

    def test_real_apps_custom_iterable_has_empty_assertion_message(self):

        class CustomIter:

            def __iter__(self):
                yield 'contenttypes'
        self._assert_assertion_message_empty(CustomIter())

    def test_real_apps_empty_list_has_empty_assertion_message(self):
        self._assert_assertion_message_empty([])

    def test_real_apps_empty_tuple_has_empty_assertion_message(self):
        self._assert_assertion_message_empty(())

    def test_real_apps_string_has_empty_assertion_message(self):
        self._assert_assertion_message_empty('contenttypes')

    def test_real_apps_int_has_empty_assertion_message(self):
        self._assert_assertion_message_empty(1)

from django.test import SimpleTestCase
from django.db.migrations.state import ProjectState

class RealAppsAssertionMessageTests(SimpleTestCase):

    def test_list_raises_assertion_no_message(self):
        with self.assertRaises(AssertionError) as cm:
            ProjectState(real_apps=['contenttypes'])
        self.assertEqual(str(cm.exception), '')

    def test_tuple_raises_assertion_no_message(self):
        with self.assertRaises(AssertionError) as cm:
            ProjectState(real_apps=('contenttypes',))
        self.assertEqual(str(cm.exception), '')

    def test_dict_raises_assertion_no_message(self):
        with self.assertRaises(AssertionError) as cm:
            ProjectState(real_apps={'contenttypes': 1})
        self.assertEqual(str(cm.exception), '')

    def test_frozenset_raises_assertion_no_message(self):
        with self.assertRaises(AssertionError) as cm:
            ProjectState(real_apps=frozenset(['contenttypes']))
        self.assertEqual(str(cm.exception), '')

    def test_generator_raises_assertion_no_message(self):
        gen = (x for x in ['contenttypes'])
        with self.assertRaises(AssertionError) as cm:
            ProjectState(real_apps=gen)
        self.assertEqual(str(cm.exception), '')

    def test_map_iterator_raises_assertion_no_message(self):
        it = map(str, ['contenttypes'])
        with self.assertRaises(AssertionError) as cm:
            ProjectState(real_apps=it)
        self.assertEqual(str(cm.exception), '')

    def test_string_raises_assertion_no_message(self):
        with self.assertRaises(AssertionError) as cm:
            ProjectState(real_apps='contenttypes')
        self.assertEqual(str(cm.exception), '')

    def test_empty_list_raises_assertion_no_message(self):
        with self.assertRaises(AssertionError) as cm:
            ProjectState(real_apps=[])
        self.assertEqual(str(cm.exception), '')

from django.test import SimpleTestCase
from django.db.migrations.state import ProjectState

class RealAppsInitTests(SimpleTestCase):

    def test_real_apps_list_raises_empty_message(self):
        with self.assertRaisesRegex(AssertionError, '^$'):
            ProjectState(real_apps=['contenttypes'])

    def test_real_apps_tuple_raises_empty_message(self):
        with self.assertRaisesRegex(AssertionError, '^$'):
            ProjectState(real_apps=('contenttypes',))

    def test_real_apps_frozenset_raises_empty_message(self):
        with self.assertRaisesRegex(AssertionError, '^$'):
            ProjectState(real_apps=frozenset({'contenttypes'}))

    def test_real_apps_generator_raises_empty_message(self):
        gen = (x for x in ['contenttypes'])
        with self.assertRaisesRegex(AssertionError, '^$'):
            ProjectState(real_apps=gen)

    def test_real_apps_map_raises_empty_message(self):
        m = map(lambda x: x, ['contenttypes'])
        with self.assertRaisesRegex(AssertionError, '^$'):
            ProjectState(real_apps=m)

    def test_real_apps_empty_list_raises_empty_message(self):
        with self.assertRaisesRegex(AssertionError, '^$'):
            ProjectState(real_apps=[])

    def test_real_apps_empty_tuple_raises_empty_message(self):
        with self.assertRaisesRegex(AssertionError, '^$'):
            ProjectState(real_apps=())

    def test_real_apps_range_raises_empty_message(self):
        with self.assertRaisesRegex(AssertionError, '^$'):
            ProjectState(real_apps=range(1))

    def test_real_apps_iterator_raises_empty_message(self):
        it = iter(['contenttypes'])
        with self.assertRaisesRegex(AssertionError, '^$'):
            ProjectState(real_apps=it)

from django.test import SimpleTestCase
from django.db.migrations.state import ProjectState
from django.test import SimpleTestCase
from django.db.migrations.state import ProjectState

class RealAppsInitRegressionTests(SimpleTestCase):

    def test_real_apps_list_raises_assertion_no_message(self):
        self._assert_assertion_has_no_message(['contenttypes'])

    def test_real_apps_tuple_raises_assertion_no_message(self):
        self._assert_assertion_has_no_message(('contenttypes',))

    def test_real_apps_frozenset_raises_assertion_no_message(self):
        self._assert_assertion_has_no_message(frozenset(['contenttypes']))

    def test_real_apps_generator_raises_assertion_no_message(self):
        gen = (x for x in ['contenttypes'])
        self._assert_assertion_has_no_message(gen)

    def test_real_apps_empty_list_raises_assertion_no_message(self):
        self._assert_assertion_has_no_message([])

    def test_real_apps_range_raises_assertion_no_message(self):
        self._assert_assertion_has_no_message(range(1))

    def test_real_apps_map_raises_assertion_no_message(self):
        self._assert_assertion_has_no_message(map(str, ['contenttypes']))

    def test_real_apps_custom_iterable_raises_assertion_no_message(self):

        class MyIterable:

            def __iter__(self):
                yield 'contenttypes'
        self._assert_assertion_has_no_message(MyIterable())

    def test_real_apps_bytes_raises_assertion_no_message(self):
        self._assert_assertion_has_no_message(b'contenttypes')

from django.test import SimpleTestCase
from django.db.migrations.state import ProjectState

class RealAppsAssertionMessageTests(SimpleTestCase):

    def test_real_apps_list_has_no_message(self):
        self._assert_no_message_assertion(['contenttypes'])

    def test_real_apps_tuple_has_no_message(self):
        self._assert_no_message_assertion(('contenttypes',))

    def test_real_apps_dict_has_no_message(self):
        self._assert_no_message_assertion({'contenttypes': True})

    def test_real_apps_generator_has_no_message(self):
        self._assert_no_message_assertion((x for x in ('contenttypes',)))

    def test_real_apps_empty_list_has_no_message(self):
        self._assert_no_message_assertion([])

    def test_real_apps_empty_tuple_has_no_message(self):
        self._assert_no_message_assertion(())

    def test_real_apps_string_has_no_message(self):
        self._assert_no_message_assertion('contenttypes')

    def test_real_apps_bytes_has_no_message(self):
        self._assert_no_message_assertion(b'contenttypes')

    def test_real_apps_frozenset_has_no_message(self):
        self._assert_no_message_assertion(frozenset({'contenttypes'}))

    def test_real_apps_range_has_no_message(self):
        self._assert_no_message_assertion(range(1))

from django.test import SimpleTestCase
from django.db.migrations.state import ProjectState
import types

class RealAppsInitTests(SimpleTestCase):

    def test_real_apps_list_assertion_message_empty(self):
        with self.assertRaises(AssertionError) as cm:
            ProjectState(real_apps=['contenttypes'])
        self.assertEqual(str(cm.exception), '')

    def test_real_apps_tuple_assertion_message_empty(self):
        with self.assertRaises(AssertionError) as cm:
            ProjectState(real_apps=('contenttypes',))
        self.assertEqual(str(cm.exception), '')

    def test_real_apps_string_assertion_message_empty(self):
        with self.assertRaises(AssertionError) as cm:
            ProjectState(real_apps='contenttypes')
        self.assertEqual(str(cm.exception), '')

    def test_real_apps_int_assertion_message_empty(self):
        with self.assertRaises(AssertionError) as cm:
            ProjectState(real_apps=123)
        self.assertEqual(str(cm.exception), '')

    def test_real_apps_frozenset_assertion_message_empty(self):
        with self.assertRaises(AssertionError) as cm:
            ProjectState(real_apps=frozenset(['contenttypes']))
        self.assertEqual(str(cm.exception), '')

    def test_real_apps_dict_assertion_message_empty(self):
        with self.assertRaises(AssertionError) as cm:
            ProjectState(real_apps={'contenttypes': True})
        self.assertEqual(str(cm.exception), '')

    def test_real_apps_generator_assertion_message_empty(self):
        gen = (x for x in ['contenttypes'])
        with self.assertRaises(AssertionError) as cm:
            ProjectState(real_apps=gen)
        self.assertEqual(str(cm.exception), '')

from django.test import SimpleTestCase
from django.db.migrations.state import ProjectState

class ProjectStateRealAppsMessageTests(SimpleTestCase):

    def test_list_real_apps_raises_assertion_with_empty_message(self):
        self.assert_assertion_message_empty_for(['contenttypes'])

    def test_tuple_real_apps_raises_assertion_with_empty_message(self):
        self.assert_assertion_message_empty_for(('contenttypes',))

    def test_frozenset_real_apps_raises_assertion_with_empty_message(self):
        self.assert_assertion_message_empty_for(frozenset({'contenttypes'}))

    def test_generator_real_apps_raises_assertion_with_empty_message(self):
        gen = (x for x in ['contenttypes'])
        self.assert_assertion_message_empty_for(gen)

    def test_string_real_apps_raises_assertion_with_empty_message(self):
        self.assert_assertion_message_empty_for('contenttypes')

    def test_int_real_apps_raises_assertion_with_empty_message(self):
        self.assert_assertion_message_empty_for(42)

    def test_dict_real_apps_raises_assertion_with_empty_message(self):
        self.assert_assertion_message_empty_for({'contenttypes': True})

    def test_empty_list_real_apps_raises_assertion_with_empty_message(self):
        self.assert_assertion_message_empty_for([])

    def test_range_real_apps_raises_assertion_with_empty_message(self):
        self.assert_assertion_message_empty_for(range(1))

from django.test import SimpleTestCase
from django.db.migrations.state import ProjectState

class ProjectStateRealAppsTypeTests(SimpleTestCase):

    def test_real_apps_list_raises_empty_message_assertion(self):
        self._assert_assertion_with_empty_message(['contenttypes'])

    def test_real_apps_tuple_raises_empty_message_assertion(self):
        self._assert_assertion_with_empty_message(('contenttypes',))

    def test_real_apps_dict_raises_empty_message_assertion(self):
        self._assert_assertion_with_empty_message({'contenttypes': 1})

    def test_real_apps_frozenset_raises_empty_message_assertion(self):
        self._assert_assertion_with_empty_message(frozenset(['contenttypes']))

    def test_real_apps_generator_raises_empty_message_assertion(self):
        gen = (x for x in ['contenttypes'])
        self._assert_assertion_with_empty_message(gen)

    def test_real_apps_string_raises_empty_message_assertion(self):
        self._assert_assertion_with_empty_message('contenttypes')

    def test_real_apps_int_raises_empty_message_assertion(self):
        self._assert_assertion_with_empty_message(123)

    def test_real_apps_bool_raises_empty_message_assertion(self):
        self._assert_assertion_with_empty_message(True)

    def test_real_apps_bytes_raises_empty_message_assertion(self):
        self._assert_assertion_with_empty_message(b'contenttypes')