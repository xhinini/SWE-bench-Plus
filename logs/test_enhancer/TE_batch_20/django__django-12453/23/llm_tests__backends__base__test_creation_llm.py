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

import contextlib
import contextlib
from unittest import mock
from django.test import SimpleTestCase
from django.db import connection

class TestDeserializeDbFromStringConstraintHandling(SimpleTestCase):
    databases = {'default'}

    def test_deserialize_constraints_with_two_objects(self):
        events = []
        objs = [self._make_obj('save1', events), self._make_obj('save2', events)]
        with mock.patch('django.core.serializers.deserialize', new=self._make_deserialize(objs)):
            connection.constraint_checks_disabled = self._make_cm(events)
            connection.check_constraints = mock.MagicMock(side_effect=lambda: events.append('check_constraints'))
            connection.creation.deserialize_db_from_string('[]')
        self.assertEqual(events, ['constraint_enter', 'save1', 'save2', 'constraint_exit', 'check_constraints'])
        connection.check_constraints.assert_called_once()

    def test_deserialize_constraints_with_one_object(self):
        events = []
        objs = [self._make_obj('save1', events)]
        with mock.patch('django.core.serializers.deserialize', new=self._make_deserialize(objs)):
            connection.constraint_checks_disabled = self._make_cm(events)
            connection.check_constraints = mock.MagicMock(side_effect=lambda: events.append('check_constraints'))
            connection.creation.deserialize_db_from_string('[]')
        self.assertEqual(events, ['constraint_enter', 'save1', 'constraint_exit', 'check_constraints'])
        connection.check_constraints.assert_called_once()

    def test_deserialize_constraints_with_no_objects(self):
        events = []
        objs = []
        with mock.patch('django.core.serializers.deserialize', new=self._make_deserialize(objs)):
            connection.constraint_checks_disabled = self._make_cm(events)
            connection.check_constraints = mock.MagicMock(side_effect=lambda: events.append('check_constraints'))
            connection.creation.deserialize_db_from_string('[]')
        self.assertEqual(events, ['constraint_enter', 'constraint_exit', 'check_constraints'])
        connection.check_constraints.assert_called_once()

    def test_deserialize_constraints_with_three_objects(self):
        events = []
        objs = [self._make_obj('save1', events), self._make_obj('save2', events), self._make_obj('save3', events)]
        with mock.patch('django.core.serializers.deserialize', new=self._make_deserialize(objs)):
            connection.constraint_checks_disabled = self._make_cm(events)
            connection.check_constraints = mock.MagicMock(side_effect=lambda: events.append('check_constraints'))
            connection.creation.deserialize_db_from_string('[]')
        self.assertEqual(events, ['constraint_enter', 'save1', 'save2', 'save3', 'constraint_exit', 'check_constraints'])
        connection.check_constraints.assert_called_once()

    def test_deserialize_constraints_with_four_objects(self):
        events = []
        objs = [self._make_obj(f'save{i}', events) for i in range(1, 5)]
        with mock.patch('django.core.serializers.deserialize', new=self._make_deserialize(objs)):
            connection.constraint_checks_disabled = self._make_cm(events)
            connection.check_constraints = mock.MagicMock(side_effect=lambda: events.append('check_constraints'))
            connection.creation.deserialize_db_from_string('[]')
        self.assertEqual(events, ['constraint_enter', 'save1', 'save2', 'save3', 'save4', 'constraint_exit', 'check_constraints'])
        connection.check_constraints.assert_called_once()

    def test_deserialize_constraints_with_five_objects(self):
        events = []
        objs = [self._make_obj(f'save{i}', events) for i in range(1, 6)]
        with mock.patch('django.core.serializers.deserialize', new=self._make_deserialize(objs)):
            connection.constraint_checks_disabled = self._make_cm(events)
            connection.check_constraints = mock.MagicMock(side_effect=lambda: events.append('check_constraints'))
            connection.creation.deserialize_db_from_string('[]')
        self.assertEqual(events, ['constraint_enter'] + [f'save{i}' for i in range(1, 6)] + ['constraint_exit', 'check_constraints'])
        connection.check_constraints.assert_called_once()

    def test_deserialize_constraints_with_six_objects(self):
        events = []
        objs = [self._make_obj(f'save{i}', events) for i in range(1, 7)]
        with mock.patch('django.core.serializers.deserialize', new=self._make_deserialize(objs)):
            connection.constraint_checks_disabled = self._make_cm(events)
            connection.check_constraints = mock.MagicMock(side_effect=lambda: events.append('check_constraints'))
            connection.creation.deserialize_db_from_string('[]')
        expected = ['constraint_enter'] + [f'save{i}' for i in range(1, 7)] + ['constraint_exit', 'check_constraints']
        self.assertEqual(events, expected)
        connection.check_constraints.assert_called_once()

    def test_deserialize_constraints_with_seven_objects(self):
        events = []
        objs = [self._make_obj(f'save{i}', events) for i in range(1, 8)]
        with mock.patch('django.core.serializers.deserialize', new=self._make_deserialize(objs)):
            connection.constraint_checks_disabled = self._make_cm(events)
            connection.check_constraints = mock.MagicMock(side_effect=lambda: events.append('check_constraints'))
            connection.creation.deserialize_db_from_string('[]')
        expected = ['constraint_enter'] + [f'save{i}' for i in range(1, 8)] + ['constraint_exit', 'check_constraints']
        self.assertEqual(events, expected)
        connection.check_constraints.assert_called_once()

    def test_deserialize_constraints_with_eight_objects(self):
        events = []
        objs = [self._make_obj(f'save{i}', events) for i in range(1, 9)]
        with mock.patch('django.core.serializers.deserialize', new=self._make_deserialize(objs)):
            connection.constraint_checks_disabled = self._make_cm(events)
            connection.check_constraints = mock.MagicMock(side_effect=lambda: events.append('check_constraints'))
            connection.creation.deserialize_db_from_string('[]')
        expected = ['constraint_enter'] + [f'save{i}' for i in range(1, 9)] + ['constraint_exit', 'check_constraints']
        self.assertEqual(events, expected)
        connection.check_constraints.assert_called_once()

    def test_deserialize_constraints_with_nine_objects(self):
        events = []
        objs = [self._make_obj(f'save{i}', events) for i in range(1, 10)]
        with mock.patch('django.core.serializers.deserialize', new=self._make_deserialize(objs)):
            connection.constraint_checks_disabled = self._make_cm(events)
            connection.check_constraints = mock.MagicMock(side_effect=lambda: events.append('check_constraints'))
            connection.creation.deserialize_db_from_string('[]')
        expected = ['constraint_enter'] + [f'save{i}' for i in range(1, 10)] + ['constraint_exit', 'check_constraints']
        self.assertEqual(events, expected)
        connection.check_constraints.assert_called_once()

import copy
from unittest import mock
from django.db import connections, DEFAULT_DB_ALIAS, connection
from django.test import SimpleTestCase
from ..models import Object, ObjectReference
import contextlib

def get_connection_copy():
    test_connection = copy.copy(connections[DEFAULT_DB_ALIAS])
    test_connection.settings_dict = copy.deepcopy(connections[DEFAULT_DB_ALIAS].settings_dict)
    return test_connection

from unittest import mock
from django.db import connection
from django.test import SimpleTestCase

class TestDeserializeConstraintHandling(SimpleTestCase):
    databases = {'default'}
    circular_data = '\n    [\n        {\n            "model": "backends.object",\n            "pk": 1,\n            "fields": {"obj_ref": 1, "related_objects": []}\n        },\n        {\n            "model": "backends.objectreference",\n            "pk": 1,\n            "fields": {"obj": 1}\n        }\n    ]\n    '

    def _make_cm(self):
        """
        Return a MagicMock context manager whose __enter__ records a flag and
        whose __exit__ is a MagicMock as well.
        """
        cm = mock.MagicMock()

        def enter_side_effect(*args, **kwargs):
            cm.entered = True
            return None
        cm.__enter__ = mock.MagicMock(side_effect=enter_side_effect)
        cm.__exit__ = mock.MagicMock(return_value=None)
        return cm

    def test_constraint_and_check_called_circular_reference(self):
        cm = self._make_cm()
        with mock.patch.object(connection, 'constraint_checks_disabled', return_value=cm) as mocked_ctx, mock.patch.object(connection, 'check_constraints') as mocked_check:
            connection.creation.deserialize_db_from_string(self.circular_data)
            mocked_ctx.assert_called_once()
            self.assertTrue(cm.__enter__.called)
            self.assertTrue(cm.__exit__.called)
            mocked_check.assert_called_once()

    def test_constraint_and_check_called_empty_list(self):
        cm = self._make_cm()
        with mock.patch.object(connection, 'constraint_checks_disabled', return_value=cm) as mocked_ctx, mock.patch.object(connection, 'check_constraints') as mocked_check:
            connection.creation.deserialize_db_from_string('[]')
            mocked_ctx.assert_called_once()
            self.assertTrue(cm.__enter__.called)
            self.assertTrue(cm.__exit__.called)
            mocked_check.assert_called_once()

    def test_constraint_and_check_called_reverse_order(self):
        reverse_data = '\n        [\n            {\n                "model": "backends.objectreference",\n                "pk": 1,\n                "fields": {"obj": 1}\n            },\n            {\n                "model": "backends.object",\n                "pk": 1,\n                "fields": {"obj_ref": 1, "related_objects": []}\n            }\n        ]\n        '
        cm = self._make_cm()
        with mock.patch.object(connection, 'constraint_checks_disabled', return_value=cm) as mocked_ctx, mock.patch.object(connection, 'check_constraints') as mocked_check:
            connection.creation.deserialize_db_from_string(reverse_data)
            mocked_ctx.assert_called_once()
            self.assertTrue(cm.__enter__.called)
            self.assertTrue(cm.__exit__.called)
            mocked_check.assert_called_once()

    def test_check_constraints_called_once_for_single_call(self):
        cm = self._make_cm()
        with mock.patch.object(connection, 'constraint_checks_disabled', return_value=cm), mock.patch.object(connection, 'check_constraints') as mocked_check:
            connection.creation.deserialize_db_from_string(self.circular_data)
            mocked_check.assert_called_once()

    def test_constraint_context_enter_and_exit_called(self):
        cm = self._make_cm()
        with mock.patch.object(connection, 'constraint_checks_disabled', return_value=cm):
            connection.creation.deserialize_db_from_string(self.circular_data)
            self.assertTrue(cm.__enter__.called)
            self.assertTrue(cm.__exit__.called)

    def test_check_constraints_called_twice_on_two_calls(self):
        cm1 = self._make_cm()
        cm2 = self._make_cm()
        with mock.patch.object(connection, 'constraint_checks_disabled', side_effect=[cm1, cm2]), mock.patch.object(connection, 'check_constraints') as mocked_check:
            connection.creation.deserialize_db_from_string(self.circular_data)
            connection.creation.deserialize_db_from_string(self.circular_data)
            self.assertEqual(mocked_check.call_count, 2)

    def test_constraint_and_check_called_with_whitespace_data(self):
        cm = self._make_cm()
        with mock.patch.object(connection, 'constraint_checks_disabled', return_value=cm), mock.patch.object(connection, 'check_constraints') as mocked_check:
            connection.creation.deserialize_db_from_string(self.circular_data)
            self.assertTrue(cm.__enter__.called)
            self.assertTrue(cm.__exit__.called)
            mocked_check.assert_called_once()

    def test_constraint_context_called_when_serialized_string_from_serialize_db_to_string(self):
        cm = self._make_cm()
        with mock.patch.object(connection, 'constraint_checks_disabled', return_value=cm), mock.patch.object(connection, 'check_constraints') as mocked_check:
            serialized = connection.creation.serialize_db_to_string()
            connection.creation.deserialize_db_from_string(serialized)
            mocked_check.assert_called()

    def test_constraint_context_and_check_called_for_multiple_objects(self):
        multiple_data = '[' + ','.join([self.circular_data.strip()[1:-1]] * 3) + ']'
        cm = self._make_cm()
        with mock.patch.object(connection, 'constraint_checks_disabled', return_value=cm), mock.patch.object(connection, 'check_constraints') as mocked_check:
            connection.creation.deserialize_db_from_string(multiple_data)
            self.assertTrue(cm.__enter__.called)
            self.assertTrue(cm.__exit__.called)
            mocked_check.assert_called_once()

from unittest import mock
from django.db import IntegrityError, connection, transaction
from django.test import SimpleTestCase
from ..models import Object, ObjectReference

class TestDeserializeDbFromStringRegression(SimpleTestCase):
    databases = {'default'}

    def setUp(self):
        ObjectReference.objects.all().delete()
        Object.objects.all().delete()

    def test_check_constraints_and_context_manager_are_called(self):
        data = '\n        [\n            {\n                "model": "backends.objectreference",\n                "pk": 1,\n                "fields": {"obj": 1}\n            },\n            {\n                "model": "backends.object",\n                "pk": 1,\n                "fields": {"obj_ref": 1, "related_objects": []}\n            }\n        ]\n        '
        mock_check = mock.MagicMock()
        fake_ctx = mock.MagicMock()
        fake_ctx.__enter__.return_value = None
        fake_ctx.__exit__.return_value = None
        with mock.patch.object(connection, 'constraint_checks_disabled', return_value=fake_ctx) as mock_ctx_mgr:
            with mock.patch.object(connection, 'check_constraints', mock_check):
                connection.creation.deserialize_db_from_string(data)
                mock_ctx_mgr.assert_called_once()
                fake_ctx.__enter__.assert_called_once()
                mock_check.assert_called_once()

    def test_constraint_checks_disabled_context_entered(self):
        data = '\n        [\n            {\n                "model": "backends.objectreference",\n                "pk": 1,\n                "fields": {"obj": 1}\n            },\n            {\n                "model": "backends.object",\n                "pk": 1,\n                "fields": {"obj_ref": 1, "related_objects": []}\n            }\n        ]\n        '
        fake_ctx = mock.MagicMock()
        fake_ctx.__enter__.return_value = None
        fake_ctx.__exit__.return_value = None
        with mock.patch.object(connection, 'constraint_checks_disabled', return_value=fake_ctx):
            connection.creation.deserialize_db_from_string(data)
            fake_ctx.__exit__.assert_called_once()

from unittest import mock
from django.test import SimpleTestCase
from django.db import connection

class TestDeserializeInvokesConstraintChecks(SimpleTestCase):
    """
    A suite of regression tests ensuring deserialize_db_from_string:
    - enters the connection.constraint_checks_disabled() context manager
    - calls connection.check_constraints() after deserializing and saving objects
    """

    def _make_cm(self):
        cm = mock.MagicMock()
        cm.__enter__ = mock.Mock(return_value=None)
        cm.__exit__ = mock.Mock(return_value=None)
        return cm

from unittest import mock
from django.db import connection
from django.test import SimpleTestCase
from ..models import Object, ObjectReference

class TestDeserializeDbFromStringExtra(SimpleTestCase):
    databases = {'default'}

    def test_check_constraints_called_empty(self):
        data = '[]'
        with mock.patch.object(connection, 'check_constraints') as mocked_check:
            connection.creation.deserialize_db_from_string(data)
            mocked_check.assert_called_once()

    def test_check_constraints_called_with_objects(self):
        data = '\n        [\n            {\n                "model": "backends.object",\n                "pk": 1,\n                "fields": {"obj_ref": 1, "related_objects": []}\n            },\n            {\n                "model": "backends.objectreference",\n                "pk": 1,\n                "fields": {"obj": 1}\n            }\n        ]\n        '
        with mock.patch.object(connection, 'check_constraints') as mocked_check:
            connection.creation.deserialize_db_from_string(data)
            mocked_check.assert_called_once()

    def test_constraint_checks_disabled_used_empty(self):
        entered = {'value': False}

        def factory():

            class DummyCM:

                def __enter__(self_inner):
                    entered['value'] = True
                    return None

                def __exit__(self_inner, exc_type, exc, tb):
                    return False
            return DummyCM()
        with mock.patch.object(connection, 'constraint_checks_disabled', new=factory):
            connection.creation.deserialize_db_from_string('[]')
            self.assertTrue(entered['value'])

    def test_constraint_checks_disabled_used_with_objects(self):
        entered = {'value': False}

        def factory():

            class DummyCM:

                def __enter__(self_inner):
                    entered['value'] = True
                    return None

                def __exit__(self_inner, exc_type, exc, tb):
                    return False
            return DummyCM()
        data = '\n        [\n            {\n                "model": "backends.object",\n                "pk": 1,\n                "fields": {"obj_ref": 1, "related_objects": []}\n            },\n            {\n                "model": "backends.objectreference",\n                "pk": 1,\n                "fields": {"obj": 1}\n            }\n        ]\n        '
        with mock.patch.object(connection, 'constraint_checks_disabled', new=factory):
            connection.creation.deserialize_db_from_string(data)
            self.assertTrue(entered['value'])

    def test_check_constraints_called_once_with_multiple_objects(self):
        data = '\n        [\n            {\n                "model": "backends.object",\n                "pk": 4,\n                "fields": {"obj_ref": 4, "related_objects": []}\n            },\n            {\n                "model": "backends.objectreference",\n                "pk": 4,\n                "fields": {"obj": 4}\n            },\n            {\n                "model": "backends.objectreference",\n                "pk": 5,\n                "fields": {"obj": 4}\n            }\n        ]\n        '
        with mock.patch.object(connection, 'check_constraints') as mocked_check:
            connection.creation.deserialize_db_from_string(data)
            mocked_check.assert_called_once()

    def test_constraint_checks_disabled_and_check_constraints_together(self):
        entered = {'value': False}

        def factory():

            class DummyCM:

                def __enter__(self_inner):
                    entered['value'] = True
                    return None

                def __exit__(self_inner, exc_type, exc, tb):
                    return False
            return DummyCM()
        data = '\n        [\n            {\n                "model": "backends.object",\n                "pk": 6,\n                "fields": {"obj_ref": 6, "related_objects": []}\n            },\n            {\n                "model": "backends.objectreference",\n                "pk": 6,\n                "fields": {"obj": 6}\n            }\n        ]\n        '
        with mock.patch.object(connection, 'constraint_checks_disabled', new=factory):
            with mock.patch.object(connection, 'check_constraints') as mocked_check:
                connection.creation.deserialize_db_from_string(data)
                self.assertTrue(entered['value'])
                mocked_check.assert_called_once()

from django.db import connections, DEFAULT_DB_ALIAS
import copy
import types
from unittest import mock
from django.db import connection
from django.test import SimpleTestCase
from django.core import serializers
from django.db import connections, DEFAULT_DB_ALIAS
import copy

def get_connection_copy_for_tests():
    test_connection = copy.copy(connections[DEFAULT_DB_ALIAS])
    test_connection.settings_dict = copy.deepcopy(connections[DEFAULT_DB_ALIAS].settings_dict)
    return test_connection

import importlib
from unittest import mock
import importlib
from unittest import mock
from django.db import connection
from django.test import SimpleTestCase
CIRCULAR_DATA = '\n[\n    {\n        "model": "backends.object",\n        "pk": 1,\n        "fields": {"obj_ref": 1, "related_objects": []}\n    },\n    {\n        "model": "backends.objectreference",\n        "pk": 1,\n        "fields": {"obj": 1}\n    }\n]\n'

class TestDeserializeDbFromStringRegression(SimpleTestCase):
    databases = {'default'}

    def _install_wrappers(self):
        """
        Wrap atomic, constraint_checks_disabled and check_constraints to record
        calls and preserve original behaviour.
        Returns a dict with control objects and a restore function.
        """
        creation_mod = importlib.import_module('django.db.backends.base.creation')
        djtrans = importlib.import_module('django.db.transaction')
        orig_constraint_ctx = connection.constraint_checks_disabled
        orig_check_constraints = connection.check_constraints
        orig_dj_atomic = djtrans.atomic
        orig_creation_atomic = getattr(creation_mod, 'atomic', None)
        order = []
        flags = {'atomic_entered': 0, 'constraint_entered': 0, 'constraint_exited': 0, 'check_constraints_called': 0, 'using_args': []}

        def constraint_wrapper():
            orig_cm = orig_constraint_ctx()

            class CM:

                def __enter__(self_inner):
                    order.append('constraint_enter')
                    flags['constraint_entered'] += 1
                    return orig_cm.__enter__()

                def __exit__(self_inner, exc_type, exc, tb):
                    order.append('constraint_exit')
                    flags['constraint_exited'] += 1
                    return orig_cm.__exit__(exc_type, exc, tb)
            return CM()
        connection.constraint_checks_disabled = constraint_wrapper

        def wrapped_check_constraints():
            order.append('check_constraints')
            flags['check_constraints_called'] += 1
            return orig_check_constraints()
        connection.check_constraints = wrapped_check_constraints

        def make_atomic_wrapper(orig_atomic):

            def atomic_wrapper(*a, **kw):
                cm = orig_atomic(*a, **kw)

                class CM:

                    def __enter__(self_inner):
                        order.append('atomic_enter')
                        flags['atomic_entered'] += 1
                        flags['using_args'].append(kw.get('using'))
                        return cm.__enter__()

                    def __exit__(self_inner, exc_type, exc, tb):
                        order.append('atomic_exit')
                        return cm.__exit__(exc_type, exc, tb)
                return CM()
            return atomic_wrapper
        djtrans.atomic = make_atomic_wrapper(orig_dj_atomic)
        if orig_creation_atomic is not None:
            creation_mod.atomic = make_atomic_wrapper(orig_creation_atomic)

        def restore():
            connection.constraint_checks_disabled = orig_constraint_ctx
            connection.check_constraints = orig_check_constraints
            djtrans.atomic = orig_dj_atomic
            if orig_creation_atomic is not None:
                creation_mod.atomic = orig_creation_atomic
        return {'order': order, 'flags': flags, 'restore': restore, 'creation_mod': creation_mod, 'orig_creation_atomic_present': orig_creation_atomic is not None}

    def test_constraint_checks_and_check_constraints_called(self):
        control = self._install_wrappers()
        try:
            connection.creation.deserialize_db_from_string(CIRCULAR_DATA)
            self.assertGreater(control['flags']['constraint_entered'], 0)
            self.assertGreater(control['flags']['check_constraints_called'], 0)
        finally:
            control['restore']()

    def test_check_constraints_called_on_empty_data(self):
        control = self._install_wrappers()
        try:
            connection.creation.deserialize_db_from_string('[]')
            self.assertGreater(control['flags']['check_constraints_called'], 0)
            self.assertGreater(control['flags']['atomic_entered'], 0)
            self.assertGreater(control['flags']['constraint_entered'], 0)
        finally:
            control['restore']()

from contextlib import contextmanager
from contextlib import contextmanager
from unittest import mock
from django.test import SimpleTestCase
from django.db import connection
from ..models import Object, ObjectReference

class TestDeserializeCallsConstraintChecks(SimpleTestCase):
    databases = {'default'}

    def test_constraints_called_circular_reference(self):
        data = '\n        [\n            {\n                "model": "backends.object",\n                "pk": 1,\n                "fields": {"obj_ref": 1, "related_objects": []}\n            },\n            {\n                "model": "backends.objectreference",\n                "pk": 1,\n                "fields": {"obj": 1}\n            }\n        ]\n        '
        self._assert_constraints_called(data)

    def test_constraints_called_single_object(self):
        data = '\n        [\n            {\n                "model": "backends.object",\n                "pk": 1,\n                "fields": {"obj_ref": null, "related_objects": []}\n            }\n        ]\n        '
        self._assert_constraints_called(data)

    def test_constraints_called_multiple_objects(self):
        data = '\n        [\n            {\n                "model": "backends.object",\n                "pk": 1,\n                "fields": {"obj_ref": null, "related_objects": []}\n            },\n            {\n                "model": "backends.object",\n                "pk": 2,\n                "fields": {"obj_ref": null, "related_objects": []}\n            },\n            {\n                "model": "backends.objectreference",\n                "pk": 1,\n                "fields": {"obj": 1}\n            }\n        ]\n        '
        self._assert_constraints_called(data)

    def test_constraints_called_empty_list(self):
        data = '[]'
        self._assert_constraints_called(data)

    def test_constraints_called_whitespace_only(self):
        data = '  \n  []  \n '
        self._assert_constraints_called(data)

    def test_constraints_called_child_before_parent(self):
        data = '\n        [\n            {\n                "model": "backends.objectreference",\n                "pk": 1,\n                "fields": {"obj": 1}\n            },\n            {\n                "model": "backends.object",\n                "pk": 1,\n                "fields": {"obj_ref": 1, "related_objects": []}\n            }\n        ]\n        '
        self._assert_constraints_called(data)

    def test_constraints_called_non_sequential_pks(self):
        data = '\n        [\n            {\n                "model": "backends.object",\n                "pk": 2,\n                "fields": {"obj_ref": null, "related_objects": []}\n            },\n            {\n                "model": "backends.object",\n                "pk": 1,\n                "fields": {"obj_ref": null, "related_objects": []}\n            },\n            {\n                "model": "backends.objectreference",\n                "pk": 2,\n                "fields": {"obj": 2}\n            }\n        ]\n        '
        self._assert_constraints_called(data)

    def test_constraints_called_many_relations(self):
        data = '\n        [\n            {\n                "model": "backends.object",\n                "pk": 1,\n                "fields": {"obj_ref": null, "related_objects": []}\n            },\n            {\n                "model": "backends.object",\n                "pk": 2,\n                "fields": {"obj_ref": 1, "related_objects": []}\n            },\n            {\n                "model": "backends.objectreference",\n                "pk": 1,\n                "fields": {"obj": 2}\n            },\n            {\n                "model": "backends.objectreference",\n                "pk": 2,\n                "fields": {"obj": 1}\n            }\n        ]\n        '
        self._assert_constraints_called(data)

    def test_constraints_called_with_extra_whitespace_and_newlines(self):
        data = '\n\n\n        [\n\n            {\n                "model": "backends.object",\n                "pk": 1,\n                "fields": {"obj_ref": null, "related_objects": []}\n            }\n\n        ]\n\n\n        '
        self._assert_constraints_called(data)

from django.test import SimpleTestCase
from .test_creation import get_connection_copy
import types
from unittest import mock
from django.db import connection
from django.core import serializers

class TestDeserializeDbConstraintHandling(SimpleTestCase):
    databases = {'default'}

    def test_constraint_checks_disabled_called(self):
        conn = connection
        cm = self._make_cm_toggle(conn)
        conn.constraint_checks_disabled = mock.MagicMock(return_value=cm)
        with mock.patch('django.core.serializers.deserialize', return_value=iter(())):
            conn.creation.deserialize_db_from_string('[]')
        conn.constraint_checks_disabled.assert_called_once()

    def test_check_constraints_called(self):
        conn = connection
        conn.check_constraints = mock.MagicMock()
        with mock.patch('django.core.serializers.deserialize', return_value=iter(())):
            conn.creation.deserialize_db_from_string('[]')
        conn.check_constraints.assert_called_once()

    def test_constraint_disabled_before_save(self):
        conn = connection
        conn._constraint_checks_disabled_active = False
        cm = self._make_cm_toggle(conn)
        conn.constraint_checks_disabled = mock.MagicMock(return_value=cm)

        class FakeObj:

            def save(self_inner, *args, **kwargs):
                if not getattr(conn, '_constraint_checks_disabled_active', False):
                    raise AssertionError('Constraint checks were not disabled during save()')
        with mock.patch('django.core.serializers.deserialize', return_value=iter([FakeObj()])):
            conn.creation.deserialize_db_from_string('[]')

    def test_check_constraints_called_after_save(self):
        conn = connection
        ops = []
        cm = self._make_cm_toggle(conn)
        conn.constraint_checks_disabled = mock.MagicMock(return_value=cm)

        class FakeObj:

            def __init__(self, idx):
                self.idx = idx

            def save(self_inner, *args, **kwargs):
                ops.append(('save', self_inner.idx))

        def fake_check_constraints():
            ops.append(('check', None))
        conn.check_constraints = mock.MagicMock(side_effect=fake_check_constraints)
        with mock.patch('django.core.serializers.deserialize', return_value=iter([FakeObj(1), FakeObj(2)])):
            conn.creation.deserialize_db_from_string('[]')
        assert ops[-1][0] == 'check'
        assert ops[0] == ('save', 1)
        assert ops[1] == ('save', 2)

    def test_constraint_context_exit_on_exception(self):
        conn = connection
        conn._cm_exit_called = False
        cm = self._make_cm_toggle(conn)
        conn.constraint_checks_disabled = mock.MagicMock(return_value=cm)

        class BadObj:

            def save(self_inner, *args, **kwargs):
                raise ValueError('boom')
        with mock.patch('django.core.serializers.deserialize', return_value=iter([BadObj()])):
            with self.assertRaises(ValueError):
                conn.creation.deserialize_db_from_string('[]')
        self.assertTrue(getattr(conn, '_cm_exit_called', False))

    def test_empty_data_still_calls_constraint_and_check(self):
        conn = connection
        conn.check_constraints = mock.MagicMock()
        cm = self._make_cm_toggle(conn)
        conn.constraint_checks_disabled = mock.MagicMock(return_value=cm)
        with mock.patch('django.core.serializers.deserialize', return_value=iter(())):
            conn.creation.deserialize_db_from_string('\n  \n')
        conn.constraint_checks_disabled.assert_called_once()
        conn.check_constraints.assert_called_once()

    def test_multiple_objects_save_order_with_checks(self):
        conn = connection
        ops = []
        cm = self._make_cm_toggle(conn)
        conn.constraint_checks_disabled = mock.MagicMock(return_value=cm)

        class FakeObj:

            def __init__(self, name):
                self.name = name

            def save(self_inner, *args, **kwargs):
                ops.append(self_inner.name)

        def fake_check():
            ops.append('check')
        conn.check_constraints = mock.MagicMock(side_effect=fake_check)
        with mock.patch('django.core.serializers.deserialize', return_value=iter([FakeObj('a'), FakeObj('b'), FakeObj('c')])):
            conn.creation.deserialize_db_from_string('[]')
        self.assertEqual(ops, ['a', 'b', 'c', 'check'])

    def test_deserialize_uses_module_level_atomic(self):
        import django.db.backends.base.creation as creation_mod
        with mock.patch.object(creation_mod, 'atomic', wraps=creation_mod.atomic) as mocked_atomic:
            with mock.patch('django.core.serializers.deserialize', return_value=iter(())):
                connection.creation.deserialize_db_from_string('[]')
            mocked_atomic.assert_called_once_with(using=connection.alias)

    def test_check_constraints_called_on_connection_copy(self):
        test_connection = get_connection_copy()
        test_connection.check_constraints = mock.MagicMock()
        cm = self._make_cm_toggle(test_connection)
        test_connection.constraint_checks_disabled = mock.MagicMock(return_value=cm)
        creation = test_connection.creation_class(test_connection)
        with mock.patch('django.core.serializers.deserialize', return_value=iter(())):
            creation.deserialize_db_from_string('[]')
        test_connection.constraint_checks_disabled.assert_called_once()
        test_connection.check_constraints.assert_called_once()

    def test_constraint_manager_used_with_whitespace_data(self):
        conn = connection
        conn.check_constraints = mock.MagicMock()
        cm = self._make_cm_toggle(conn)
        conn.constraint_checks_disabled = mock.MagicMock(return_value=cm)
        with mock.patch('django.core.serializers.deserialize', return_value=iter(())):
            conn.creation.deserialize_db_from_string('  \n  ')
        conn.constraint_checks_disabled.assert_called_once()
        conn.check_constraints.assert_called_once()

from unittest import mock
from unittest import mock
from django.test import SimpleTestCase
from django.db import connection
from django.db.backends.base.creation import BaseDatabaseCreation
try:
    get_connection_copy
except NameError:
    import copy
    from django.db import connections, DEFAULT_DB_ALIAS

    def get_connection_copy():
        test_connection = copy.copy(connections[DEFAULT_DB_ALIAS])
        test_connection.settings_dict = copy.deepcopy(connections[DEFAULT_DB_ALIAS].settings_dict)
        return test_connection

class TestDeserializeConstraintHandling(SimpleTestCase):
    databases = {'default'}

    def test_uses_constraint_checks_disabled_and_calls_check_constraints_on_default_connection(self):
        entered = []

        class CM:

            def __enter__(self):
                entered.append('enter')
                return self

            def __exit__(self, exc_type, exc, tb):
                entered.append('exit')
        with mock.patch.object(connection, 'constraint_checks_disabled', return_value=CM()) as mocked_cm, mock.patch.object(connection, 'check_constraints') as mocked_check, mock.patch('django.db.backends.base.creation.serializers.deserialize', return_value=iter([])) as mocked_deser:
            connection.creation.deserialize_db_from_string('[]')
        self.assertIn('enter', entered)
        self.assertIn('exit', entered)
        mocked_check.assert_called_once()
        mocked_deser.assert_called()

    def test_uses_constraint_checks_disabled_and_calls_check_constraints_on_custom_connection(self):
        test_conn = get_connection_copy()
        entered = []

        class CM:

            def __enter__(self):
                entered.append('enter')
                return self

            def __exit__(self, exc_type, exc, tb):
                entered.append('exit')
        creation = BaseDatabaseCreation(test_conn)
        with mock.patch.object(test_conn, 'constraint_checks_disabled', return_value=CM()) as mocked_cm, mock.patch.object(test_conn, 'check_constraints') as mocked_check, mock.patch('django.db.backends.base.creation.serializers.deserialize', return_value=iter([])) as mocked_deser:
            creation.deserialize_db_from_string('[]')
        self.assertIn('enter', entered)
        self.assertIn('exit', entered)
        mocked_check.assert_called_once()
        mocked_deser.assert_called()

    def test_constraint_checks_disabled_called_on_creation_instance(self):
        test_conn = get_connection_copy()
        creation = BaseDatabaseCreation(test_conn)
        entered = []

        class CM:

            def __enter__(self):
                entered.append(True)
                return self

            def __exit__(self, exc_type, exc, tb):
                entered.append(False)
        with mock.patch.object(test_conn, 'constraint_checks_disabled', return_value=CM()), mock.patch.object(test_conn, 'check_constraints') as mocked_check, mock.patch('django.db.backends.base.creation.serializers.deserialize', return_value=iter([])):
            creation.deserialize_db_from_string('[]')
        self.assertEqual(entered, [True, False])
        mocked_check.assert_called_once()