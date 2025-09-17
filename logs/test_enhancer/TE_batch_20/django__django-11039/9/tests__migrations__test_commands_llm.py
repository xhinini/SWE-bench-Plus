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

from types import SimpleNamespace

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_sqlmigrate_other_db_non_transactional_forwards(self):
    """
    sqlmigrate for a non-transactional 'other' DB should not show BEGIN/COMMIT.
    """
    out = io.StringIO()
    with mock.patch.object(connections['other'].features, 'can_rollback_ddl', False):
        call_command('sqlmigrate', 'migrations', '0001', stdout=out, database='other')
    output = out.getvalue().lower()
    queries = [q.strip() for q in output.splitlines()]
    start_transaction_sql = connections['other'].ops.start_transaction_sql()
    if start_transaction_sql:
        self.assertNotIn(start_transaction_sql.lower(), queries)
    self.assertNotIn(connections['other'].ops.end_transaction_sql().lower(), queries)

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_sqlmigrate_other_db_transactional_forwards(self):
    """
    sqlmigrate for a transactional 'other' DB should show BEGIN/COMMIT around atomic migration.
    """
    out = io.StringIO()
    with mock.patch.object(connections['other'].features, 'can_rollback_ddl', True):
        call_command('sqlmigrate', 'migrations', '0001', stdout=out, database='other')
    output = out.getvalue().lower()
    index_tx_start = output.find(connections['other'].ops.start_transaction_sql().lower())
    index_op_desc_author = output.find('-- create model author')
    index_create_table = output.find('create table')
    index_op_desc_tribble = output.find('-- create model tribble')
    index_op_desc_unique_together = output.find('-- alter unique_together')
    index_tx_end = output.find(connections['other'].ops.end_transaction_sql().lower())
    if connections['other'].ops.start_transaction_sql():
        self.assertGreater(index_tx_start, -1, 'Transaction start not found for other db')
        self.assertGreater(index_tx_end, index_op_desc_unique_together, 'Transaction end not found or found before operation description (unique_together) for other db')
    self.assertGreater(index_op_desc_author, index_tx_start)
    self.assertGreater(index_create_table, index_op_desc_author)
    self.assertGreater(index_op_desc_tribble, index_create_table)
    self.assertGreater(index_op_desc_unique_together, index_op_desc_tribble)

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_sqlmigrate_other_db_non_transactional_backwards(self):
    """
    sqlmigrate --backwards for a non-transactional 'other' DB should not show BEGIN/COMMIT.
    """
    call_command('migrate', 'migrations', verbosity=0, database='other')
    out = io.StringIO()
    with mock.patch.object(connections['other'].features, 'can_rollback_ddl', False):
        call_command('sqlmigrate', 'migrations', '0001', stdout=out, backwards=True, database='other')
    output = out.getvalue().lower()
    queries = [q.strip() for q in output.splitlines()]
    start_transaction_sql = connections['other'].ops.start_transaction_sql()
    if start_transaction_sql:
        self.assertNotIn(start_transaction_sql.lower(), queries)
    self.assertNotIn(connections['other'].ops.end_transaction_sql().lower(), queries)

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_sqlmigrate_other_db_transactional_backwards(self):
    """
    sqlmigrate --backwards for a transactional 'other' DB should show BEGIN/COMMIT.
    """
    call_command('migrate', 'migrations', verbosity=0, database='other')
    out = io.StringIO()
    with mock.patch.object(connections['other'].features, 'can_rollback_ddl', True):
        call_command('sqlmigrate', 'migrations', '0001', stdout=out, backwards=True, database='other')
    output = out.getvalue().lower()
    index_tx_start = output.find(connections['other'].ops.start_transaction_sql().lower())
    index_op_desc_unique_together = output.find('-- alter unique_together')
    index_op_desc_tribble = output.find('-- create model tribble')
    index_op_desc_author = output.find('-- create model author')
    index_drop_table = output.rfind('drop table')
    index_tx_end = output.find(connections['other'].ops.end_transaction_sql().lower())
    if connections['other'].ops.start_transaction_sql():
        self.assertGreater(index_tx_start, -1, 'Transaction start not found for other db (backwards)')
        self.assertGreater(index_tx_end, index_op_desc_unique_together, 'Transaction end not found or found before DROP TABLE for other db (backwards)')
    self.assertGreater(index_op_desc_unique_together, index_tx_start)
    self.assertGreater(index_op_desc_tribble, index_op_desc_unique_together)
    self.assertGreater(index_op_desc_author, index_op_desc_tribble)
    self.assertGreater(index_drop_table, index_op_desc_author)

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations_non_atomic'})
def test_sqlmigrate_for_non_atomic_migration_on_other_db(self):
    """
    Non-atomic migration on 'other' DB should not show transaction wrappers even if DB supports them.
    """
    out = io.StringIO()
    with mock.patch.object(connections['other'].features, 'can_rollback_ddl', True):
        call_command('sqlmigrate', 'migrations', '0001', stdout=out, database='other')
    output = out.getvalue().lower()
    queries = [q.strip() for q in output.splitlines()]
    if connections['other'].ops.start_transaction_sql():
        self.assertNotIn(connections['other'].ops.start_transaction_sql().lower(), queries)
    self.assertNotIn(connections['other'].ops.end_transaction_sql().lower(), queries)

def test_handle_sets_output_transaction_false_when_db_non_transactional(self):
    """
    Unit-level test: when migration.atomic is True but the DB's can_rollback_ddl is False,
    handle() should set self.output_transaction to False.
    """
    app_label = 'migrations'
    migration_name = '0001'
    migration_obj = SimpleNamespace(name=migration_name, atomic=True)

    class FakeLoader:

        def __init__(self):
            self.migrated_apps = {app_label}
            self._migration = migration_obj
            self.graph = SimpleNamespace(nodes={(app_label, migration_name): 'node'})

        def get_migration_by_prefix(self, a_label, prefix):
            return self._migration

    class FakeExecutor:

        def __init__(self, connection):
            self.loader = FakeLoader()

        def collect_sql(self, plan):
            return ['SELECT 1']
    with mock.patch('django.db.migrations.executor.MigrationExecutor', new=FakeExecutor):
        with mock.patch.object(connections['default'].features, 'can_rollback_ddl', False):
            cmd = __import__('django.core.management.commands.sqlmigrate', fromlist=['Command']).Command()
            result = cmd.handle(app_label=app_label, migration_name=migration_name, database='default', backwards=False)
            self.assertFalse(cmd.output_transaction)
            self.assertEqual(result, 'select 1')

def test_handle_sets_output_transaction_true_when_both_true(self):
    """
    Unit-level test: when migration.atomic and DB.can_rollback_ddl are both True,
    handle() should set self.output_transaction to True.
    """
    app_label = 'migrations'
    migration_name = '0001'
    migration_obj = SimpleNamespace(name=migration_name, atomic=True)

    class FakeLoader:

        def __init__(self):
            self.migrated_apps = {app_label}
            self._migration = migration_obj
            self.graph = SimpleNamespace(nodes={(app_label, migration_name): 'node'})

        def get_migration_by_prefix(self, a_label, prefix):
            return self._migration

    class FakeExecutor:

        def __init__(self, connection):
            self.loader = FakeLoader()

        def collect_sql(self, plan):
            return ['SELECT 1']
    with mock.patch('django.db.migrations.executor.MigrationExecutor', new=FakeExecutor):
        with mock.patch.object(connections['default'].features, 'can_rollback_ddl', True):
            cmd = __import__('django.core.management.commands.sqlmigrate', fromlist=['Command']).Command()
            result = cmd.handle(app_label=app_label, migration_name=migration_name, database='default', backwards=False)
            self.assertTrue(cmd.output_transaction)
            self.assertEqual(result, 'select 1')

def test_handle_uses_specified_database_connection(self):
    """
    Unit-level test: handle() should consult the specified database's features.
    """
    app_label = 'migrations'
    migration_name = '0001'
    migration_obj = SimpleNamespace(name=migration_name, atomic=True)

    class FakeLoader:

        def __init__(self):
            self.migrated_apps = {app_label}
            self._migration = migration_obj
            self.graph = SimpleNamespace(nodes={(app_label, migration_name): 'node'})

        def get_migration_by_prefix(self, a_label, prefix):
            return self._migration

    class FakeExecutor:

        def __init__(self, connection):
            self.loader = FakeLoader()

        def collect_sql(self, plan):
            return ['SELECT 1']
    with mock.patch('django.db.migrations.executor.MigrationExecutor', new=FakeExecutor):
        with mock.patch.object(connections['default'].features, 'can_rollback_ddl', False):
            with mock.patch.object(connections['other'].features, 'can_rollback_ddl', True):
                cmd = __import__('django.core.management.commands.sqlmigrate', fromlist=['Command']).Command()
                res_default = cmd.handle(app_label=app_label, migration_name=migration_name, database='default', backwards=False)
                self.assertFalse(cmd.output_transaction)
                self.assertEqual(res_default, 'select 1')
                cmd2 = __import__('django.core.management.commands.sqlmigrate', fromlist=['Command']).Command()
                res_other = cmd2.handle(app_label=app_label, migration_name=migration_name, database='other', backwards=False)
                self.assertTrue(cmd2.output_transaction)
                self.assertEqual(res_other, 'select 1')