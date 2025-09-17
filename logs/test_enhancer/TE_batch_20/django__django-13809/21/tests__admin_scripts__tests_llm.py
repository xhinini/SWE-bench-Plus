from io import StringIO
from unittest import mock
from io import StringIO
from unittest import mock
from django.test import SimpleTestCase
from django.core.management import call_command
from django.core.management.commands.runserver import Command as RunserverCommand

class ManageRunserverSkipChecksRegression(SimpleTestCase):

    def setUp(self):
        self.output = StringIO()

    @mock.patch('django.core.management.commands.runserver.run')
    @mock.patch('django.core.management.base.BaseCommand.check_migrations')
    @mock.patch('django.core.management.base.BaseCommand.check')
    def test_call_command_skip_calls_check_migrations(self, mocked_check, mocked_check_migrations, mocked_run):
        call_command('runserver', use_reloader=False, skip_checks=True, stdout=self.output)
        mocked_check.assert_not_called()
        self.assertTrue(mocked_check_migrations.called)
        self.assertNotIn('Skipping system checks.', self.output.getvalue())

    @mock.patch('django.core.management.commands.runserver.run')
    @mock.patch('django.core.management.base.BaseCommand.check_migrations')
    @mock.patch('django.core.management.base.BaseCommand.check')
    def test_call_command_skip_does_not_print_skip_message(self, mocked_check, mocked_check_migrations, mocked_run):
        self.output.truncate(0)
        self.output.seek(0)
        call_command('runserver', use_reloader=False, skip_checks=True, stdout=self.output)
        out = self.output.getvalue()
        self.assertNotIn('Skipping system checks.', out)
        self.assertNotIn('Performing system checks...', out)

from io import StringIO
from unittest import mock
from django.core.management import call_command
from django.test import SimpleTestCase
from django.db.migrations.recorder import MigrationRecorder

class RunserverSkipChecksTests(SimpleTestCase):

    def setUp(self):
        self.output = StringIO()

from io import StringIO
from unittest import mock
from io import StringIO
from unittest import mock
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.core.management.commands.runserver import Command as RunserverCommand
from django.test import SimpleTestCase

class RunserverSkipChecksRegressionTests(SimpleTestCase):

    def setUp(self):
        self.output = StringIO()

def test_check_migrations_called_with_skip_checks_true(self):
    """check_migrations is called even when skip_checks=True."""
    self.output.truncate(0)
    self.output.seek(0)
    with mock.patch('django.core.management.commands.runserver.run') as mock_run:
        with mock.patch('django.core.management.base.BaseCommand.check_migrations') as mock_check_migrations:
            call_command('runserver', use_reloader=False, skip_checks=True, stdout=self.output)
    mock_check_migrations.assert_called_once()

def test_check_migrations_called_with_skip_checks_false(self):
    """check_migrations is called when skip_checks=False."""
    self.output.truncate(0)
    self.output.seek(0)
    with mock.patch('django.core.management.commands.runserver.run') as mock_run:
        with mock.patch('django.core.management.base.BaseCommand.check_migrations') as mock_check_migrations:
            call_command('runserver', use_reloader=False, skip_checks=False, stdout=self.output)
    mock_check_migrations.assert_called_once()

def test_no_skipping_message_with_skip_checks_true(self):
    """
    Ensure no misleading "Skipping system checks." message is printed when
    skip_checks=True, and that the "Performing system checks..." message is
    not printed either (since system checks are skipped).
    """
    self.output.truncate(0)
    self.output.seek(0)
    with mock.patch('django.core.management.commands.runserver.run'):
        with mock.patch('django.core.management.base.BaseCommand.check_migrations'):
            call_command('runserver', use_reloader=False, skip_checks=True, stdout=self.output)
    out = self.output.getvalue()
    self.assertNotIn('Skipping system checks.', out)
    self.assertNotIn('Performing system checks...', out)

def test_performing_message_with_skip_checks_false(self):
    """Ensure "Performing system checks..." is printed when skip_checks=False."""
    self.output.truncate(0)
    self.output.seek(0)
    with mock.patch('django.core.management.commands.runserver.run'):
        with mock.patch('django.core.management.base.BaseCommand.check_migrations'):
            call_command('runserver', use_reloader=False, skip_checks=False, stdout=self.output)
    out = self.output.getvalue()
    self.assertIn('Performing system checks...', out)

def test_check_migrations_called_before_run_when_not_skipped(self):
    """
    Ensure check_migrations runs before the server run() is invoked when
    skip_checks=False.
    """
    order = []

    def record_check_migrations(*a, **k):
        order.append('check_migrations')

    def record_run(*a, **k):
        order.append('run')
    self.output.truncate(0)
    self.output.seek(0)
    with mock.patch('django.core.management.base.BaseCommand.check_migrations', side_effect=record_check_migrations):
        with mock.patch('django.core.management.commands.runserver.run', side_effect=record_run):
            call_command('runserver', use_reloader=False, skip_checks=False, stdout=self.output)
    self.assertEqual(order, ['check_migrations', 'run'])

def test_check_migrations_called_before_run_when_skipped_flag_true(self):
    """
    Even when system checks are skipped (skip_checks=True), check_migrations
    should still run and happen before the server run() invocation.
    """
    order = []

    def record_check_migrations(*a, **k):
        order.append('check_migrations')

    def record_run(*a, **k):
        order.append('run')
    self.output.truncate(0)
    self.output.seek(0)
    with mock.patch('django.core.management.base.BaseCommand.check_migrations', side_effect=record_check_migrations):
        with mock.patch('django.core.management.commands.runserver.run', side_effect=record_run):
            call_command('runserver', use_reloader=False, skip_checks=True, stdout=self.output)
    self.assertEqual(order, ['check_migrations', 'run'])

def test_check_skipped_but_migrations_run(self):
    """
    When skip_checks=True, BaseCommand.check should not be called, but
    BaseCommand.check_migrations must be called.
    """
    self.output.truncate(0)
    self.output.seek(0)
    with mock.patch('django.core.management.commands.runserver.run'):
        with mock.patch('django.core.management.base.BaseCommand.check') as mock_check:
            with mock.patch('django.core.management.base.BaseCommand.check_migrations') as mock_check_migrations:
                call_command('runserver', use_reloader=False, skip_checks=True, stdout=self.output)
    mock_check.assert_not_called()
    mock_check_migrations.assert_called_once()

def test_check_called_and_migrations_run_when_not_skipped(self):
    """
    When skip_checks=False, both BaseCommand.check and
    BaseCommand.check_migrations must be called.
    """
    self.output.truncate(0)
    self.output.seek(0)
    with mock.patch('django.core.management.commands.runserver.run'):
        with mock.patch('django.core.management.base.BaseCommand.check') as mock_check:
            with mock.patch('django.core.management.base.BaseCommand.check_migrations') as mock_check_migrations:
                call_command('runserver', use_reloader=False, skip_checks=False, stdout=self.output)
    mock_check.assert_called_once()
    mock_check_migrations.assert_called_once()

def test_migration_message_present_when_migrations_indicate_work(self):
    """
    If check_migrations writes migration warnings, those should appear even
    when skip_checks=True (verifying migrations were executed).
    """

    def fake_check_migrations(self_obj):
        self_obj.stdout.write('You have 1 unapplied migration(s).')
    self.output.truncate(0)
    self.output.seek(0)
    with mock.patch('django.core.management.commands.runserver.run'):
        with mock.patch('django.core.management.base.BaseCommand.check_migrations', fake_check_migrations):
            call_command('runserver', use_reloader=False, skip_checks=True, stdout=self.output)
    out = self.output.getvalue()
    self.assertIn('You have 1 unapplied migration(s)', out)

from io import StringIO
from unittest import mock
from django.core.management import call_command
from django.core.management.commands.runserver import Command as RunserverCommand
from django.core.management.base import BaseCommand
from django.test import SimpleTestCase
from django.db.migrations.recorder import MigrationRecorder

from io import StringIO
import socket
import unittest
from unittest import mock
from django.test import SimpleTestCase
from django.core.management import call_command

class RunserverSkipChecksRegressionTests(SimpleTestCase):

    def setUp(self):
        self.output = StringIO()

    @mock.patch('django.core.management.commands.runserver.run')
    @mock.patch('django.core.management.base.BaseCommand.check_migrations')
    @mock.patch('django.core.management.base.BaseCommand.check')
    def test_check_migrations_called_with_addrport(self, mock_check, mock_check_migrations, mock_run):
        call_command('runserver', addrport='7000', use_reloader=False, skip_checks=True, stdout=self.output)
        mock_check.assert_not_called()
        mock_check_migrations.assert_called()

    @mock.patch('django.core.management.commands.runserver.run')
    @mock.patch('django.core.management.base.BaseCommand.check_migrations')
    @mock.patch('django.core.management.base.BaseCommand.check')
    def test_check_migrations_called_with_hostname(self, mock_check, mock_check_migrations, mock_run):
        call_command('runserver', addrport='localhost:8000', use_reloader=False, skip_checks=True, stdout=self.output)
        mock_check.assert_not_called()
        mock_check_migrations.assert_called()

    @unittest.skipUnless(socket.has_ipv6, "platform doesn't support IPv6")
    @mock.patch('django.core.management.commands.runserver.run')
    @mock.patch('django.core.management.base.BaseCommand.check_migrations')
    @mock.patch('django.core.management.base.BaseCommand.check')
    def test_check_migrations_called_with_use_ipv6_flag(self, mock_check, mock_check_migrations, mock_run):
        call_command('runserver', use_ipv6=True, use_reloader=False, skip_checks=True, stdout=self.output)
        mock_check.assert_not_called()
        mock_check_migrations.assert_called()

    @unittest.skipUnless(socket.has_ipv6, "platform doesn't support IPv6")
    @mock.patch('django.core.management.commands.runserver.run')
    @mock.patch('django.core.management.base.BaseCommand.check_migrations')
    @mock.patch('django.core.management.base.BaseCommand.check')
    def test_check_migrations_called_with_ipv6_literal(self, mock_check, mock_check_migrations, mock_run):
        call_command('runserver', addrport='[::1]:8000', use_reloader=False, skip_checks=True, stdout=self.output)
        mock_check.assert_not_called()
        mock_check_migrations.assert_called()

    @unittest.skipUnless(socket.has_ipv6, "platform doesn't support IPv6")
    @mock.patch('django.core.management.commands.runserver.run')
    @mock.patch('django.core.management.base.BaseCommand.check_migrations')
    @mock.patch('django.core.management.base.BaseCommand.check')
    def test_check_migrations_called_with_raw_ipv6(self, mock_check, mock_check_migrations, mock_run):
        call_command('runserver', addrport='[2001:db8::1]:7000', use_reloader=False, skip_checks=True, stdout=self.output)
        mock_check.assert_not_called()
        mock_check_migrations.assert_called()

    @mock.patch('django.core.management.commands.runserver.run')
    @mock.patch('django.core.management.base.BaseCommand.check_migrations')
    @mock.patch('django.core.management.base.BaseCommand.check')
    def test_check_migrations_called_with_no_color(self, mock_check, mock_check_migrations, mock_run):
        call_command('runserver', use_reloader=False, skip_checks=True, no_color=True, stdout=self.output)
        mock_check.assert_not_called()
        mock_check_migrations.assert_called()

    @mock.patch('django.core.management.commands.runserver.run')
    @mock.patch('django.core.management.base.BaseCommand.check_migrations')
    @mock.patch('django.core.management.base.BaseCommand.check')
    def test_check_migrations_called_with_threading_disabled(self, mock_check, mock_check_migrations, mock_run):
        call_command('runserver', use_reloader=False, skip_checks=True, use_threading=False, stdout=self.output)
        mock_check.assert_not_called()
        mock_check_migrations.assert_called()

    @mock.patch('django.core.management.commands.runserver.run')
    @mock.patch('django.core.management.base.BaseCommand.check_migrations')
    @mock.patch('django.core.management.base.BaseCommand.check')
    def test_check_migrations_called_when_default_addr_and_skip_checks_true(self, mock_check, mock_check_migrations, mock_run):
        call_command('runserver', use_reloader=False, skip_checks=True, stdout=self.output)
        mock_check.assert_not_called()
        mock_check_migrations.assert_called()

from io import StringIO
from unittest import mock
from io import StringIO
from unittest import mock
from django.test import SimpleTestCase
from django.core.management.commands.runserver import Command as RunserverCommand

class RunserverInnerRunSkipChecksTests(SimpleTestCase):

    def setUp(self):
        self.stdout = StringIO()
        self.cmd = RunserverCommand(stdout=self.stdout)

from io import StringIO
from django.test import SimpleTestCase
from django.core.management import call_command
from django.core.management.commands.runserver import Command as RunserverCommand
from unittest import mock

class ManageRunserverSkipChecksTests(SimpleTestCase):

    def setUp(self):

        def monkey_run(*args, **options):
            return
        self.output = StringIO()
        self.cmd = RunserverCommand(stdout=self.output)
        self.cmd.run = monkey_run

from io import StringIO
from unittest import mock
from django.core.management import call_command
from django.core.management.commands.runserver import Command as RunserverCommand
from django.test import SimpleTestCase
import django.utils.autoreload

class ManageRunserverSkipChecksTests(SimpleTestCase):

    def setUp(self):
        self.output = StringIO()

    def test_call_command_skip_checks_calls_check_migrations_and_no_messages(self):
        with mock.patch('django.core.management.commands.runserver.run') as mocked_run:
            with mock.patch('django.core.management.base.BaseCommand.check_migrations') as mocked_check_migrations:
                with mock.patch('django.core.management.base.BaseCommand.check') as mocked_check:
                    call_command('runserver', use_reloader=False, skip_checks=True, stdout=self.output)
                    out = self.output.getvalue()
                    self.assertNotIn('Performing system checks...', out)
                    self.assertNotIn('Skipping system checks.', out)
                    mocked_check.assert_not_called()
                    self.assertTrue(mocked_check_migrations.called)

    def test_call_command_skip_checks_with_threading_true_calls_check_migrations(self):
        with mock.patch('django.core.management.commands.runserver.run') as mocked_run:
            with mock.patch('django.core.management.base.BaseCommand.check_migrations') as mocked_check_migrations:
                with mock.patch('django.core.management.base.BaseCommand.check') as mocked_check:
                    call_command('runserver', use_reloader=False, skip_checks=True, use_threading=True, stdout=self.output)
                    out = self.output.getvalue()
                    self.assertNotIn('Performing system checks...', out)
                    self.assertNotIn('Skipping system checks.', out)
                    mocked_check.assert_not_called()
                    self.assertTrue(mocked_check_migrations.called)