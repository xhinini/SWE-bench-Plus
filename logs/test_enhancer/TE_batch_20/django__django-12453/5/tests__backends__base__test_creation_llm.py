import django.db.backends.base.creation as creation
import types
from unittest import mock
from django.test import SimpleTestCase
from django.db import connection
import django.db.backends.base.creation as creation

class TestDeserializeDbConstraintManagement(SimpleTestCase):
    databases = {'default'}

    def test_constraint_checks_disabled_enter_called(self):
        cm = mock.MagicMock()
        cm.__enter__.side_effect = lambda: True
        with mock.patch.object(connection, 'constraint_checks_disabled', return_value=cm) as mock_constraint, mock.patch('django.db.backends.base.creation.serializers.deserialize', return_value=[]) as mock_deserialize:
            connection.creation.deserialize_db_from_string('[]')
            cm.__enter__.assert_called_once()
            mock_constraint.assert_called_once()

    def test_constraint_checks_disabled_exit_called(self):
        cm = mock.MagicMock()
        cm.__exit__.side_effect = lambda *args: False
        with mock.patch.object(connection, 'constraint_checks_disabled', return_value=cm):
            with mock.patch('django.db.backends.base.creation.serializers.deserialize', return_value=[]):
                connection.creation.deserialize_db_from_string('[]')
                cm.__exit__.assert_called_once()

    def test_check_constraints_called(self):
        with mock.patch.object(connection, 'check_constraints') as mock_check, mock.patch.object(connection, 'constraint_checks_disabled', return_value=mock.MagicMock()) as mock_constraint, mock.patch('django.db.backends.base.creation.serializers.deserialize', return_value=[]):
            connection.creation.deserialize_db_from_string('[]')
            mock_check.assert_called_once()

    def test_save_called_inside_constraint_disabled_context(self):
        order = []
        cm = mock.MagicMock()
        cm.__enter__.side_effect = lambda: order.append('enter')
        cm.__exit__.side_effect = lambda *args: order.append('exit')

        def save():
            order.append('save')
        fake_obj = self._make_fake_obj(save)
        with mock.patch.object(connection, 'constraint_checks_disabled', return_value=cm), mock.patch.object(connection, 'check_constraints', return_value=None) as mock_check, mock.patch('django.db.backends.base.creation.serializers.deserialize', return_value=[fake_obj]):
            connection.creation.deserialize_db_from_string('[]')
            self.assertEqual(order, ['enter', 'save', 'exit'])
            mock_check.assert_called_once()

    def test_multiple_objects_all_saved_and_checks_called_once(self):
        order = []
        cm = mock.MagicMock()
        cm.__enter__.side_effect = lambda: order.append('enter')
        cm.__exit__.side_effect = lambda *args: order.append('exit')

        def make_save(i):
            return lambda: order.append(f'save{i}')
        objs = [self._make_fake_obj(make_save(i)) for i in (1, 2, 3)]
        with mock.patch.object(connection, 'constraint_checks_disabled', return_value=cm), mock.patch.object(connection, 'check_constraints') as mock_check, mock.patch('django.db.backends.base.creation.serializers.deserialize', return_value=objs):
            connection.creation.deserialize_db_from_string('[]')
            self.assertEqual(order, ['enter', 'save1', 'save2', 'save3', 'exit'])
            mock_check.assert_called_once()

    def test_no_objects_still_calls_constraint_manager_and_check_constraints(self):
        cm = mock.MagicMock()
        cm.__enter__.side_effect = lambda: True
        cm.__exit__.side_effect = lambda *args: True
        with mock.patch.object(connection, 'constraint_checks_disabled', return_value=cm) as mock_constraint, mock.patch.object(connection, 'check_constraints') as mock_check, mock.patch('django.db.backends.base.creation.serializers.deserialize', return_value=[]):
            connection.creation.deserialize_db_from_string('[]')
            cm.__enter__.assert_called_once()
            cm.__exit__.assert_called_once()
            mock_check.assert_called_once()

    def test_context_enter_before_any_save_order(self):
        sequence = []
        cm = mock.MagicMock()
        cm.__enter__.side_effect = lambda: sequence.append('enter')
        cm.__exit__.side_effect = lambda *args: sequence.append('exit')
        save_mock = mock.MagicMock(side_effect=lambda: sequence.append('save'))
        fake_obj = self._make_fake_obj(save_mock)
        with mock.patch.object(connection, 'constraint_checks_disabled', return_value=cm), mock.patch.object(connection, 'check_constraints', return_value=None), mock.patch('django.db.backends.base.creation.serializers.deserialize', return_value=[fake_obj]):
            connection.creation.deserialize_db_from_string('[]')
            self.assertEqual(sequence, ['enter', 'save', 'exit'])

    def test_exit_before_check_constraints_order(self):
        sequence = []
        cm = mock.MagicMock()
        cm.__enter__.side_effect = lambda: sequence.append('enter')
        cm.__exit__.side_effect = lambda *args: sequence.append('exit')

        def save():
            sequence.append('save')
        fake_obj = self._make_fake_obj(save)

        def check_constraints_side_effect():
            sequence.append('check')
        with mock.patch.object(connection, 'constraint_checks_disabled', return_value=cm), mock.patch.object(connection, 'check_constraints', side_effect=check_constraints_side_effect) as mock_check, mock.patch('django.db.backends.base.creation.serializers.deserialize', return_value=[fake_obj]):
            connection.creation.deserialize_db_from_string('[]')
            self.assertEqual(sequence, ['enter', 'save', 'exit', 'check'])
            mock_check.assert_called_once()

    def test_check_constraints_called_once_with_multiple_objects(self):
        cm = mock.MagicMock()
        cm.__enter__.side_effect = lambda: True
        cm.__exit__.side_effect = lambda *args: True
        objs = [self._make_fake_obj(lambda: None) for _ in range(5)]
        with mock.patch.object(connection, 'constraint_checks_disabled', return_value=cm), mock.patch.object(connection, 'check_constraints') as mock_check, mock.patch('django.db.backends.base.creation.serializers.deserialize', return_value=objs):
            connection.creation.deserialize_db_from_string('[]')
            mock_check.assert_called_once()

    def test_module_level_atomic_called(self):
        with mock.patch('django.db.backends.base.creation.atomic', create=True) as mock_atomic, mock.patch.object(connection, 'constraint_checks_disabled', return_value=mock.MagicMock()), mock.patch.object(connection, 'check_constraints', return_value=None), mock.patch('django.db.backends.base.creation.serializers.deserialize', return_value=[]):
            connection.creation.deserialize_db_from_string('[]')
            mock_atomic.assert_called_once_with(using=connection.alias)

from django.db import connection
from django.test import SimpleTestCase
from unittest import mock
import copy
from unittest import mock
from django.db import connection
from django.test import SimpleTestCase
from ..models import Object, ObjectReference

class TestDeserializeDbFromStringAdditional(SimpleTestCase):
    databases = {'default'}

    def test_circular_reference_calls_constraint_disable_and_check_constraints(self):
        data = '\n        [\n            {\n                "model": "backends.object",\n                "pk": 1,\n                "fields": {"obj_ref": 1, "related_objects": []}\n            },\n            {\n                "model": "backends.objectreference",\n                "pk": 1,\n                "fields": {"obj": 1}\n            }\n        ]\n        '
        self._wrap_and_assert(data)
        self.assertEqual(Object.objects.count(), 1)
        self.assertEqual(ObjectReference.objects.count(), 1)

    def test_multiple_objects_calls_constraint_disable_and_check_constraints(self):
        data = '\n        [\n            {\n                "model": "backends.object",\n                "pk": 1,\n                "fields": {"obj_ref": null, "related_objects": []}\n            },\n            {\n                "model": "backends.object",\n                "pk": 2,\n                "fields": {"obj_ref": null, "related_objects": []}\n            }\n        ]\n        '
        self._wrap_and_assert(data)
        self.assertEqual(Object.objects.count(), 2)

    def test_whitespace_handling_calls_constraint_disable_and_check_constraints(self):
        data = '\n  [\n  ]\n'
        self._wrap_and_assert(data)

    def test_constraint_context_enter_and_exit_called_for_circular_reference(self):
        data = '\n        [\n            {\n                "model": "backends.object",\n                "pk": 1,\n                "fields": {"obj_ref": 1, "related_objects": []}\n            },\n            {\n                "model": "backends.objectreference",\n                "pk": 1,\n                "fields": {"obj": 1}\n            }\n        ]\n        '
        orig_constraint_checks_disabled = connection.constraint_checks_disabled
        try:
            mock_cm = mock.MagicMock()
            mock_cm.__enter__ = mock.MagicMock(return_value=None)
            mock_cm.__exit__ = mock.MagicMock(return_value=None)
            connection.constraint_checks_disabled = mock.MagicMock(return_value=mock_cm)
            connection.check_constraints = mock.MagicMock()
            connection.creation.deserialize_db_from_string(data)
            self.assertTrue(connection.constraint_checks_disabled.called)
            self.assertTrue(mock_cm.__enter__.called)
            self.assertTrue(mock_cm.__exit__.called, '__exit__ on constraint_checks_disabled() context manager was not called')
            self.assertTrue(connection.check_constraints.called)
        finally:
            connection.constraint_checks_disabled = orig_constraint_checks_disabled

    def test_check_constraints_called_once_for_circular_reference(self):
        data = '\n        [\n            {\n                "model": "backends.object",\n                "pk": 1,\n                "fields": {"obj_ref": 1, "related_objects": []}\n            },\n            {\n                "model": "backends.objectreference",\n                "pk": 1,\n                "fields": {"obj": 1}\n            }\n        ]\n        '
        orig_check_constraints = connection.check_constraints
        try:
            connection.constraint_checks_disabled = mock.MagicMock(return_value=mock.MagicMock(__enter__=mock.MagicMock(return_value=None), __exit__=mock.MagicMock(return_value=None)))
            connection.check_constraints = mock.MagicMock()
            connection.creation.deserialize_db_from_string(data)
            self.assertEqual(connection.check_constraints.call_count, 1)
        finally:
            connection.check_constraints = orig_check_constraints

    def test_constraint_checks_disabled_called_for_forward_references(self):
        data = '\n        [\n            {\n                "model": "backends.objectreference",\n                "pk": 1,\n                "fields": {"obj": 1}\n            },\n            {\n                "model": "backends.object",\n                "pk": 1,\n                "fields": {"obj_ref": 1, "related_objects": []}\n            }\n        ]\n        '
        self._wrap_and_assert(data)

    def test_constraint_checks_disabled_called_with_non_standard_spacing(self):
        data = '[{"model":"backends.object","pk":1,"fields":{"obj_ref":null,"related_objects":[]}}]'
        self._wrap_and_assert(data)

    def test_constraint_checks_disabled_called_for_large_payload(self):
        data = '\n        [\n            {\n                "model": "backends.object",\n                "pk": 1,\n                "fields": {"obj_ref": null, "related_objects": []}\n            },\n            {\n                "model": "backends.object",\n                "pk": 2,\n                "fields": {"obj_ref": null, "related_objects": []}\n            },\n            {\n                "model": "backends.objectreference",\n                "pk": 1,\n                "fields": {"obj": 1}\n            }\n        ]\n        '
        self._wrap_and_assert(data)

    def test_constraint_checks_disabled_and_check_constraints_called_when_data_has_comments_like_spacing(self):
        data = '\n\n[\n  {"model": "backends.object", "pk": 1, "fields": {"obj_ref": null, "related_objects": []}}\n]\n'
        self._wrap_and_assert(data)

import types
from unittest import mock
from django.test import SimpleTestCase
from django.db import connection
from django.core import serializers

class TestDeserializeConstraintHandling(SimpleTestCase):

    def _make_cm(self, events=None, enter_label='enter', exit_label='exit'):
        """
        Create a simple context manager mock that records enter/exit in events
        if provided.
        """
        cm = mock.MagicMock()
        if events is not None:

            def enter():
                events.append(enter_label)

            def exit(exc_type, exc, tb):
                events.append(exit_label)
                return False
            cm.__enter__.side_effect = enter
            cm.__exit__.side_effect = exit
        else:
            cm.__enter__.return_value = None
            cm.__exit__.return_value = False
        return cm

from unittest import mock
from django.test import SimpleTestCase
from django.db.backends.base.creation import BaseDatabaseCreation

class TestDeserializeDbFromStringRegression(SimpleTestCase):

    def _make_connection_with_cm(self):
        conn = mock.MagicMock()
        conn.alias = 'default'
        cm = mock.MagicMock()
        cm.__enter__ = mock.Mock(return_value=None)
        cm.__exit__ = mock.Mock(return_value=None)
        conn.constraint_checks_disabled.return_value = cm
        conn.check_constraints = mock.Mock()
        return (conn, cm)