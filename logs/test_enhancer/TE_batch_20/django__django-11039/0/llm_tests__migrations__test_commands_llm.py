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