import io
from unittest import mock
from django.core.management import call_command
from django.test import override_settings
from .test_base import MigrationTestBase
from django.db import connections

class SqlMigrateDatabaseSelectionTests(MigrationTestBase):
    """
    Tests ensuring sqlmigrate respects the --database option for deciding
    whether to output transaction wrappers.
    """
    databases = {'default', 'other'}

    @override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
    def test_sqlmigrate_specified_db_without_rollback_feature_shows_no_wrappers_backwards(self):
        """
        Same as above but for backwards SQL generation.
        """
        out = io.StringIO()
        other_conn = connections['other']
        call_command('migrate', 'migrations', verbosity=0, database='other')
        with mock.patch.object(other_conn.features, 'can_rollback_ddl', False):
            call_command('sqlmigrate', 'migrations', '0001', stdout=out, backwards=True, database='other')
            output = out.getvalue().lower()
            self.assertNotIn((other_conn.ops.start_transaction_sql() or '').lower(), output)
            self.assertNotIn((other_conn.ops.end_transaction_sql() or '').lower(), output)

from types import SimpleNamespace
from unittest import mock
from types import SimpleNamespace
from unittest import mock
from django.test import SimpleTestCase
from django.core.management.commands import sqlmigrate
from django.core.management.base import BaseCommand

def _make_fake_executor_factory(atomic, sql_statements, app_label='testapp'):
    """
    Returns a MigrationExecutor replacement class that returns a migration
    with the given `atomic` attribute and whose collect_sql returns
    `sql_statements`.
    """

    class FakeExecutor:

        def __init__(self, connection):
            self.connection = connection
            migration = SimpleNamespace(name='0001', atomic=atomic)

            def get_migration_by_prefix(a_label, migration_name):
                if a_label == app_label and migration_name.startswith('0001'):
                    return migration
                raise KeyError('migration not found')
            self.loader = SimpleNamespace(migrated_apps={app_label}, get_migration_by_prefix=get_migration_by_prefix, graph=SimpleNamespace(nodes={(app_label, migration.name): 'node'}))

        def collect_sql(self, plan):
            return list(sql_statements)
    return FakeExecutor

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_sqlmigrate_forwards_no_transaction_when_db_cannot_rollback_ddl_default(self):
    """
    Forward SQL: when the DB does not support transactional DDL, no
    transaction wrappers should be emitted even for atomic migrations.
    """
    out = io.StringIO()
    with mock.patch.object(connection.features, 'can_rollback_ddl', False):
        call_command('sqlmigrate', 'migrations', '0001', stdout=out)
    output = out.getvalue().lower()
    start_sql = connection.ops.start_transaction_sql()
    if start_sql:
        self.assertNotIn(start_sql.lower(), output)
    self.assertNotIn(connection.ops.end_transaction_sql().lower(), output)

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_sqlmigrate_backwards_no_transaction_when_db_cannot_rollback_ddl_default(self):
    """
    Backwards SQL: when the DB does not support transactional DDL, no
    transaction wrappers should be emitted even for atomic migrations.
    """
    call_command('migrate', 'migrations', verbosity=0)
    out = io.StringIO()
    with mock.patch.object(connection.features, 'can_rollback_ddl', False):
        call_command('sqlmigrate', 'migrations', '0001', stdout=out, backwards=True)
    output = out.getvalue().lower()
    start_sql = connection.ops.start_transaction_sql()
    if start_sql:
        self.assertNotIn(start_sql.lower(), output)
    self.assertNotIn(connection.ops.end_transaction_sql().lower(), output)
    call_command('migrate', 'migrations', 'zero', verbosity=0)

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_sqlmigrate_forwards_no_transaction_when_db_cannot_rollback_ddl_other_db(self):
    """
    Forward SQL on a non-default database: no transaction wrappers when that
    database does not support transactional DDL.
    """
    out = io.StringIO()
    with mock.patch.object(connections['other'].features, 'can_rollback_ddl', False):
        call_command('sqlmigrate', 'migrations', '0001', stdout=out, database='other')
    output = out.getvalue().lower()
    start_sql = connections['other'].ops.start_transaction_sql()
    if start_sql:
        self.assertNotIn(start_sql.lower(), output)
    self.assertNotIn(connections['other'].ops.end_transaction_sql().lower(), output)

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_sqlmigrate_backwards_no_transaction_when_db_cannot_rollback_ddl_other_db(self):
    """
    Backwards SQL on a non-default database: no transaction wrappers when
    that database does not support transactional DDL.
    """
    call_command('migrate', 'migrations', '0001', verbosity=0, database='other')
    out = io.StringIO()
    with mock.patch.object(connections['other'].features, 'can_rollback_ddl', False):
        call_command('sqlmigrate', 'migrations', '0001', stdout=out, backwards=True, database='other')
    output = out.getvalue().lower()
    start_sql = connections['other'].ops.start_transaction_sql()
    if start_sql:
        self.assertNotIn(start_sql.lower(), output)
    self.assertNotIn(connections['other'].ops.end_transaction_sql().lower(), output)
    call_command('migrate', 'migrations', 'zero', verbosity=0, database='other')

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations_non_atomic'})
def test_sqlmigrate_non_atomic_never_shows_transaction_wrappers_even_if_db_supports(self):
    """
    Non-atomic migrations must never show BEGIN/COMMIT wrappers regardless
    of the database's transactional DDL support.
    """
    out = io.StringIO()
    with mock.patch.object(connection.features, 'can_rollback_ddl', True):
        call_command('sqlmigrate', 'migrations', '0001', stdout=out)
    output = out.getvalue().lower()
    start_sql = connection.ops.start_transaction_sql()
    if start_sql:
        self.assertNotIn(start_sql.lower(), output)
    self.assertNotIn(connection.ops.end_transaction_sql().lower(), output)

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_sqlmigrate_shows_wrappers_only_when_atomic_and_db_supports_for_other_db(self):
    """
    Ensure that for an atomic migration on a database that supports
    transactional DDL, transaction wrappers are present (other DB).
    """
    out = io.StringIO()
    with mock.patch.object(connections['other'].features, 'can_rollback_ddl', True), mock.patch.object(connections['other'].ops, 'start_transaction_sql', return_value='BEGIN;'), mock.patch.object(connections['other'].ops, 'end_transaction_sql', return_value='COMMIT;'):
        call_command('sqlmigrate', 'migrations', '0001', stdout=out, database='other')
    output = out.getvalue().lower()
    self.assertIn('begin;'.lower(), output)
    self.assertIn('commit;'.lower(), output)

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_sqlmigrate_no_start_when_start_sql_empty(self):
    """
    If the backend returns an empty start_transaction_sql(), no start
    wrapper should be emitted even if the migration is atomic and the DB
    claims to support transactional DDL.
    """
    out = io.StringIO()
    with mock.patch.object(connection.features, 'can_rollback_ddl', True), mock.patch.object(connection.ops, 'start_transaction_sql', return_value=''), mock.patch.object(connection.ops, 'end_transaction_sql', return_value='COMMIT;'):
        call_command('sqlmigrate', 'migrations', '0001', stdout=out)
    output = out.getvalue().lower()
    self.assertNotIn(''.lower(), output)
    self.assertIn('commit;'.lower(), output)
    self.assertNotIn('\x1b', output)

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_sqlmigrate_no_end_when_end_sql_empty(self):
    """
    If the backend returns an empty end_transaction_sql(), no end
    wrapper should be emitted even if the migration is atomic and the DB
    claims to support transactional DDL.
    """
    out = io.StringIO()
    with mock.patch.object(connection.features, 'can_rollback_ddl', True), mock.patch.object(connection.ops, 'start_transaction_sql', return_value='BEGIN;'), mock.patch.object(connection.ops, 'end_transaction_sql', return_value=''):
        call_command('sqlmigrate', 'migrations', '0001', stdout=out)
    output = out.getvalue().lower()
    self.assertIn('begin;'.lower(), output)
    self.assertNotIn(''.lower(), output)

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_sqlmigrate_no_color_forced_even_if_supports_color_true(self):
    """
    The command forces no_color=True in execute(), so even if color
    support is True, the SQL should not contain ANSI color sequences.
    """
    out = io.StringIO()
    with mock.patch('django.core.management.color.supports_color', lambda *args: True), mock.patch.object(connection.features, 'can_rollback_ddl', True), mock.patch.object(connection.ops, 'start_transaction_sql', return_value='BEGIN;'), mock.patch.object(connection.ops, 'end_transaction_sql', return_value='COMMIT;'):
        call_command('sqlmigrate', 'migrations', '0001', stdout=out, no_color=False)
    output = out.getvalue()
    self.assertNotIn('\x1b', output)