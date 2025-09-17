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