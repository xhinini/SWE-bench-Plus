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

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_sqlmigrate_respects_database_option_non_transactional(self):
    """
    When the targeted database doesn't support transactional DDL,
    sqlmigrate should not emit transaction wrappers for that database.
    """
    out = io.StringIO()
    with mock.patch.object(connections['other'].features, 'can_rollback_ddl', False):
        call_command('sqlmigrate', 'migrations', '0001', stdout=out, database='other')
    output = out.getvalue().lower()
    start = connections['other'].ops.start_transaction_sql()
    end = connections['other'].ops.end_transaction_sql()
    if start:
        self.assertNotIn(start.lower(), output)
    if end:
        self.assertNotIn(end.lower(), output)

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_sqlmigrate_respects_database_option_transactional(self):
    """
    When the targeted database supports transactional DDL and the migration
    is atomic, sqlmigrate should emit transaction wrappers for that database.
    """
    out = io.StringIO()
    with mock.patch.object(connections['other'].features, 'can_rollback_ddl', True), mock.patch.object(connections['other'].ops, 'start_transaction_sql', return_value='BEGIN;'), mock.patch.object(connections['other'].ops, 'end_transaction_sql', return_value='COMMIT;'):
        call_command('sqlmigrate', 'migrations', '0001', stdout=out, database='other')
    output = out.getvalue().lower()
    self.assertIn('begin;', output)
    self.assertIn('commit;', output)
    idx_begin = output.find('begin;')
    idx_op = output.find('-- create model author')
    idx_commit = output.find('commit;')
    self.assertGreaterEqual(idx_begin, 0)
    self.assertGreater(idx_op, idx_begin)
    self.assertGreater(idx_commit, idx_op)

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_sqlmigrate_database_backwards_non_transactional(self):
    """
    Generating reverse SQL for a migration on a non-transactional database
    should not include transaction wrappers.
    """
    call_command('migrate', 'migrations', verbosity=0, database='other')
    out = io.StringIO()
    with mock.patch.object(connections['other'].features, 'can_rollback_ddl', False):
        call_command('sqlmigrate', 'migrations', '0001', stdout=out, backwards=True, database='other')
    output = out.getvalue().lower()
    start = connections['other'].ops.start_transaction_sql()
    end = connections['other'].ops.end_transaction_sql()
    if start:
        self.assertNotIn(start.lower(), output)
    if end:
        self.assertNotIn(end.lower(), output)

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_sqlmigrate_database_backwards_transactional(self):
    """
    Generating reverse SQL for a migration on a transactional database
    should include transaction wrappers.
    """
    call_command('migrate', 'migrations', verbosity=0, database='other')
    out = io.StringIO()
    with mock.patch.object(connections['other'].features, 'can_rollback_ddl', True), mock.patch.object(connections['other'].ops, 'start_transaction_sql', return_value='BEGIN;'), mock.patch.object(connections['other'].ops, 'end_transaction_sql', return_value='COMMIT;'):
        call_command('sqlmigrate', 'migrations', '0001', stdout=out, backwards=True, database='other')
    output = out.getvalue().lower()
    self.assertIn('begin;', output)
    self.assertIn('commit;', output)
    idx_begin = output.find('begin;')
    idx_unique = output.find('-- alter unique_together')
    idx_commit = output.find('commit;')
    self.assertGreaterEqual(idx_begin, 0)
    self.assertGreater(idx_unique, idx_begin)
    self.assertGreater(idx_commit, idx_unique)

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_sqlmigrate_handles_empty_start_sql(self):
    """
    If start_transaction_sql() returns an empty string, sqlmigrate should not
    include a start wrapper even if the DB supports transactional DDL.
    """
    out = io.StringIO()
    with mock.patch.object(connection.features, 'can_rollback_ddl', True), mock.patch.object(connection.ops, 'start_transaction_sql', return_value=''), mock.patch.object(connection.ops, 'end_transaction_sql', return_value='COMMIT;'):
        call_command('sqlmigrate', 'migrations', '0001', stdout=out)
    output = out.getvalue().lower()
    self.assertNotIn('begin;', output)
    self.assertNotIn('commit;', output)

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_sqlmigrate_handles_empty_end_sql(self):
    """
    If end_transaction_sql() returns an empty string, sqlmigrate should not
    include an end wrapper even if the DB supports transactional DDL.
    """
    out = io.StringIO()
    with mock.patch.object(connection.features, 'can_rollback_ddl', True), mock.patch.object(connection.ops, 'start_transaction_sql', return_value='BEGIN;'), mock.patch.object(connection.ops, 'end_transaction_sql', return_value=''):
        call_command('sqlmigrate', 'migrations', '0001', stdout=out)
    output = out.getvalue().lower()
    self.assertNotIn('commit;', output)

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_sqlmigrate_output_transaction_state_is_per_call(self):
    """
    output_transaction should be based on the selected database's features
    for each invocation; state should not bleed between calls.
    """
    out1 = io.StringIO()
    with mock.patch.object(connections['other'].features, 'can_rollback_ddl', False):
        call_command('sqlmigrate', 'migrations', '0001', stdout=out1, database='other')
    output1 = out1.getvalue().lower()
    start_other = connections['other'].ops.start_transaction_sql()
    if start_other:
        self.assertNotIn(start_other.lower(), output1)
    out2 = io.StringIO()
    with mock.patch.object(connections['other'].features, 'can_rollback_ddl', True), mock.patch.object(connections['other'].ops, 'start_transaction_sql', return_value='BEGIN;'), mock.patch.object(connections['other'].ops, 'end_transaction_sql', return_value='COMMIT;'):
        call_command('sqlmigrate', 'migrations', '0001', stdout=out2, database='other')
    output2 = out2.getvalue().lower()
    self.assertIn('begin;', output2)
    self.assertIn('commit;', output2)

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_sqlmigrate_respects_can_rollback_default_db(self):
    """
    Default database's can_rollback_ddl False prevents transaction wrappers
    from being shown on default database.
    """
    out = io.StringIO()
    with mock.patch.object(connection.features, 'can_rollback_ddl', False):
        call_command('sqlmigrate', 'migrations', '0001', stdout=out)
    output = out.getvalue().lower()
    start = connection.ops.start_transaction_sql()
    end = connection.ops.end_transaction_sql()
    if start:
        self.assertNotIn(start.lower(), output)
    if end:
        self.assertNotIn(end.lower(), output)

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_sqlmigrate_respects_database_option_over_default_features(self):
    """
    When the default DB supports transactional DDL but the selected '--database'
    does not, sqlmigrate should use the selected database's features.
    """
    out = io.StringIO()
    with mock.patch.object(connection.features, 'can_rollback_ddl', True), mock.patch.object(connections['other'].features, 'can_rollback_ddl', False):
        call_command('sqlmigrate', 'migrations', '0001', stdout=out, database='other')
    output = out.getvalue().lower()
    start_other = connections['other'].ops.start_transaction_sql()
    if start_other:
        self.assertNotIn(start_other.lower(), output)

from unittest import mock
from types import SimpleNamespace
from django.core.management.base import BaseCommand
from django.test import TestCase
from django.db.migrations.loader import AmbiguityError
from unittest import mock
from types import SimpleNamespace
from django.core.management import CommandError
from django.core.management.base import BaseCommand
from django.test import TestCase
from django.core.management.commands.sqlmigrate import Command
from django.db.migrations.loader import AmbiguityError

class SqlMigrateRegressionTests(TestCase):
    """
    Regression tests for sqlmigrate output_transaction logic and command behavior.
    """

    def _make_executor_mock(self, migrated_apps=None, atomic=True, migration_name='0001_initial'):
        """
        Returns a Mock for MigrationExecutor that provides a loader with the
        desired migrated_apps and a migration object with the given atomic
        attribute. collect_sql returns a single SQL statement for simplicity.
        """
        migrated_apps = migrated_apps or set(['migrations'])

        def _executor_ctor(connection):
            loader = mock.MagicMock()
            loader.migrated_apps = set(migrated_apps)
            migration = mock.MagicMock()
            migration.name = migration_name
            migration.atomic = atomic
            loader.get_migration_by_prefix.return_value = migration
            loader.graph.nodes = {('migrations', migration_name): 'node'}
            exec_inst = mock.MagicMock()
            exec_inst.loader = loader
            exec_inst.collect_sql.return_value = ['SELECT 1;']
            return exec_inst
        return _executor_ctor

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_sqlmigrate_forwards_default_db_uses_can_rollback_ddl_true(self):
    """
    For the default database, when can_rollback_ddl is True and the migration
    is atomic, transaction wrappers should be present in the sqlmigrate output.
    """
    out = io.StringIO()
    with mock.patch.object(connection.features, 'can_rollback_ddl', True):
        call_command('sqlmigrate', 'migrations', '0001', stdout=out)
    output = out.getvalue().lower()
    start_sql = connection.ops.start_transaction_sql()
    end_sql = connection.ops.end_transaction_sql()
    if start_sql:
        self.assertIn(start_sql.lower(), output)
    if end_sql:
        self.assertIn(end_sql.lower(), output)

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_sqlmigrate_backwards_default_db_uses_can_rollback_ddl_true(self):
    """
    For the default database, backwards sqlmigrate should include transaction
    wrappers when can_rollback_ddl is True and the migration is atomic.
    """
    call_command('migrate', 'migrations', verbosity=0)
    out = io.StringIO()
    with mock.patch.object(connection.features, 'can_rollback_ddl', True):
        call_command('sqlmigrate', 'migrations', '0001', stdout=out, backwards=True)
    output = out.getvalue().lower()
    start_sql = connection.ops.start_transaction_sql()
    end_sql = connection.ops.end_transaction_sql()
    if start_sql:
        self.assertIn(start_sql.lower(), output)
    if end_sql:
        self.assertIn(end_sql.lower(), output)
    call_command('migrate', 'migrations', 'zero', verbosity=0)

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_sqlmigrate_forwards_default_db_uses_can_rollback_ddl_false(self):
    """
    For the default database, when can_rollback_ddl is False, transaction
    wrappers should NOT be present even if the migration is atomic.
    """
    out = io.StringIO()
    with mock.patch.object(connection.features, 'can_rollback_ddl', False):
        call_command('sqlmigrate', 'migrations', '0001', stdout=out)
    output = out.getvalue().lower()
    start_sql = connection.ops.start_transaction_sql()
    end_sql = connection.ops.end_transaction_sql()
    queries = [q.strip() for q in output.splitlines()]
    if start_sql:
        self.assertNotIn(start_sql.lower(), queries)
    if end_sql:
        self.assertNotIn(end_sql.lower(), queries)

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_sqlmigrate_backwards_default_db_uses_can_rollback_ddl_false(self):
    """
    For the default database, backwards sqlmigrate should NOT include
    transaction wrappers when can_rollback_ddl is False.
    """
    call_command('migrate', 'migrations', verbosity=0)
    out = io.StringIO()
    with mock.patch.object(connection.features, 'can_rollback_ddl', False):
        call_command('sqlmigrate', 'migrations', '0001', stdout=out, backwards=True)
    output = out.getvalue().lower()
    start_sql = connection.ops.start_transaction_sql()
    end_sql = connection.ops.end_transaction_sql()
    queries = [q.strip() for q in output.splitlines()]
    if start_sql:
        self.assertNotIn(start_sql.lower(), queries)
    if end_sql:
        self.assertNotIn(end_sql.lower(), queries)
    call_command('migrate', 'migrations', 'zero', verbosity=0)

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_sqlmigrate_forwards_other_db_uses_its_can_rollback_ddl_true(self):
    """
    When targeting the 'other' database, sqlmigrate should consult
    connections['other'].features.can_rollback_ddl.
    """
    other_conn = connections['other']
    out = io.StringIO()
    with mock.patch.object(other_conn.features, 'can_rollback_ddl', True):
        call_command('sqlmigrate', 'migrations', '0001', stdout=out, database='other')
    output = out.getvalue().lower()
    start_sql = other_conn.ops.start_transaction_sql()
    end_sql = other_conn.ops.end_transaction_sql()
    if start_sql:
        self.assertIn(start_sql.lower(), output)
    if end_sql:
        self.assertIn(end_sql.lower(), output)

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_sqlmigrate_backwards_other_db_uses_its_can_rollback_ddl_true(self):
    """
    Backwards sqlmigrate on the 'other' database should include transaction
    wrappers when that connection supports transactional DDL.
    """
    call_command('migrate', 'migrations', verbosity=0)
    call_command('migrate', 'migrations', verbosity=0, database='other')
    other_conn = connections['other']
    out = io.StringIO()
    with mock.patch.object(other_conn.features, 'can_rollback_ddl', True):
        call_command('sqlmigrate', 'migrations', '0001', stdout=out, backwards=True, database='other')
    output = out.getvalue().lower()
    start_sql = other_conn.ops.start_transaction_sql()
    end_sql = other_conn.ops.end_transaction_sql()
    if start_sql:
        self.assertIn(start_sql.lower(), output)
    if end_sql:
        self.assertIn(end_sql.lower(), output)
    call_command('migrate', 'migrations', 'zero', verbosity=0)
    call_command('migrate', 'migrations', 'zero', verbosity=0, database='other')

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
def test_sqlmigrate_forwards_other_db_uses_its_can_rollback_ddl_false(self):
    """
    When the 'other' database does NOT support transactional DDL, sqlmigrate
    should NOT include transaction wrappers for that database.
    """
    other_conn = connections['other']
    out = io.StringIO()
    with mock.patch.object(other_conn.features, 'can_rollback_ddl', False):
        call_command('sqlmigrate', 'migrations', '0001', stdout=out, database='other')
    output = out.getvalue().lower()
    start_sql = other_conn.ops.start_transaction_sql()
    end_sql = other_conn.ops.end_transaction_sql()
    queries = [q.strip() for q in output.splitlines()]
    if start_sql:
        self.assertNotIn(start_sql.lower(), queries)
    if end_sql:
        self.assertNotIn(end_sql.lower(), queries)

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations_non_atomic'})
def test_sqlmigrate_non_atomic_ignores_can_rollback_ddl_true(self):
    """
    Non-atomic migrations should never be wrapped in transaction BEGIN/COMMIT,
    even if the database supports transactional DDL.
    """
    out = io.StringIO()
    with mock.patch.object(connection.features, 'can_rollback_ddl', True):
        call_command('sqlmigrate', 'migrations', '0001', stdout=out)
    output = out.getvalue().lower()
    start_sql = connection.ops.start_transaction_sql()
    end_sql = connection.ops.end_transaction_sql()
    queries = [q.strip() for q in output.splitlines()]
    if start_sql:
        self.assertNotIn(start_sql.lower(), queries)
    if end_sql:
        self.assertNotIn(end_sql.lower(), queries)

@override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations_non_atomic'})
def test_sqlmigrate_non_atomic_and_db_false(self):
    """
    Non-atomic migrations and databases that don't support transactional
    DDL both should result in no transaction wrappers.
    """
    out = io.StringIO()
    with mock.patch.object(connection.features, 'can_rollback_ddl', False):
        call_command('sqlmigrate', 'migrations', '0001', stdout=out)
    output = out.getvalue().lower()
    start_sql = connection.ops.start_transaction_sql()
    end_sql = connection.ops.end_transaction_sql()
    queries = [q.strip() for q in output.splitlines()]
    if start_sql:
        self.assertNotIn(start_sql.lower(), queries)
    if end_sql:
        self.assertNotIn(end_sql.lower(), queries)

from unittest import mock
import io
from unittest import mock
from django.test import TestCase
from django.core.management import call_command
from django.db import connections
import io

class SqlMigrateTransactionFlagTests(TestCase):
    """
    Tests that sqlmigrate only outputs BEGIN/COMMIT transaction wrappers
    when both the migration is atomic and the database supports transactional DDL.
    """

    def test_forward_non_atomic_but_db_supports_hides_wrappers(self):
        output, conn = self._run_sqlmigrate_with_executor(atomic_flag=False, can_rollback_flag=True, backwards=False)
        self._assert_wrappers_absent(output, conn)

    def test_backwards_non_atomic_but_db_supports_hides_wrappers(self):
        output, conn = self._run_sqlmigrate_with_executor(atomic_flag=False, can_rollback_flag=True, backwards=True)
        self._assert_wrappers_absent(output, conn)

    def test_other_database_atomic_but_db_does_not_support_hides_wrappers(self):
        output, conn = self._run_sqlmigrate_with_executor(atomic_flag=True, can_rollback_flag=False, backwards=False, database='other')
        self._assert_wrappers_absent(output, conn)

import io
from unittest import mock
from django.core.management import call_command
from django.db import connections, connection
from django.test import override_settings
from .test_base import MigrationTestBase
from django.core.management.commands.sqlmigrate import Command
import io
from unittest import mock
from django.core.management import call_command
from django.db import connections, connection
from django.test import override_settings
from .test_base import MigrationTestBase
from django.core.management.commands.sqlmigrate import Command

class SqlMigrateTransactionBehaviorTests(MigrationTestBase):
    """
    Additional regression tests ensuring sqlmigrate only outputs transaction
    wrappers when both migration.atomic and connection.features.can_rollback_ddl
    are True.
    """
    databases = {'default', 'other'}

    @override_settings(MIGRATION_MODULES={'migrations': 'migrations.test_migrations'})
    def test_sqlmigrate_other_db_non_transactional_backwards(self):
        """
        Backwards SQL on a non-transactional 'other' DB must not show BEGIN/COMMIT.
        """
        call_command('migrate', 'migrations', verbosity=0, database='other')
        out = io.StringIO()
        with mock.patch.object(connections['other'].features, 'can_rollback_ddl', False):
            call_command('sqlmigrate', 'migrations', '0001', stdout=out, database='other', backwards=True)
        output = out.getvalue().lower()
        queries = [q.strip() for q in output.splitlines()]
        start = connections['other'].ops.start_transaction_sql()
        if start:
            self.assertNotIn(start.lower(), queries)
        self.assertNotIn(connections['other'].ops.end_transaction_sql().lower(), queries)

from unittest import mock
import io
import types
from django.test import TestCase, override_settings
from django.core.management import call_command, CommandError
from django.db import connections, DEFAULT_DB_ALIAS
from django.db.migrations.loader import AmbiguityError
from django.core.management.commands import sqlmigrate as sqlmigrate_module
from django.core.management.commands.sqlmigrate import Command

class SqlMigrateHandleUnitTests(TestCase):
    """
    Unit tests that patch MigrationExecutor to check that Command.handle sets
    output_transaction correctly depending on migration.atomic and the
    database connection's features.can_rollback_ddl flag.
    """

    def _make_fake_executor(self, migration_name='0001', atomic=True, sql_statements=None):
        """
        Returns a FakeExecutor class (callable) suitable for patching
        django.core.management.commands.sqlmigrate.MigrationExecutor.
        """
        if sql_statements is None:
            sql_statements = ['-- sample sql']

        class FakeMigration:

            def __init__(self, name, atomic):
                self.name = name
                self.atomic = atomic

        class FakeLoader:

            def __init__(self, migration):
                self.migrated_apps = {'migrations'}
                self._migration = migration
                self.graph = types.SimpleNamespace(nodes={('migrations', migration.name): object()})

            def get_migration_by_prefix(self, app_label, migration_name):
                if migration_name in migration.name:
                    return self._migration
                raise KeyError('not found')

        class FakeExecutor:

            def __init__(self, connection):
                self.connection = connection
                self.loader = FakeLoader(FakeMigration(migration_name, atomic))

            def collect_sql(self, plan):
                return sql_statements
        return FakeExecutor