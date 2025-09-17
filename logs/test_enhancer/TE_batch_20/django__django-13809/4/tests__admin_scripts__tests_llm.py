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