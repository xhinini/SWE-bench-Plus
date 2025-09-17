#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
export LANG=en_US.UTF-8
export LANGUAGE=en_US:en
export LC_ALL=en_US.UTF-8
export PYTHONIOENCODING=utf8
python --version && python -m pip install -U pip
python -m pip install -U 'coverage==6.2'

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_commands_llm.SqlMigrateTransactionAndErrorsTests._make_executor_mock migrations.test_commands_llm.SqlMigrateTransactionAndErrorsTests.test_ambiguityerror_raised_from_get_migration_becomes_commanderror migrations.test_commands_llm.SqlMigrateTransactionAndErrorsTests.test_app_without_migrations_raises_commanderror migrations.test_commands_llm.SqlMigrateTransactionAndErrorsTests.test_database_argument_passed_to_migrationexecutor migrations.test_commands_llm.SqlMigrateTransactionAndErrorsTests.test_execute_forces_no_color_option migrations.test_commands_llm.SqlMigrateTransactionAndErrorsTests.test_keyerror_from_get_migration_becomes_commanderror migrations.test_commands_llm.SqlMigrateTransactionAndErrorsTests.test_no_wrappers_when_atomic_but_db_does_not_support migrations.test_commands_llm.SqlMigrateTransactionAndErrorsTests.test_no_wrappers_when_non_atomic_even_if_db_supports migrations.test_commands_llm.SqlMigrateTransactionAndErrorsTests.test_output_transaction_when_atomic_and_db_supports migrations.test_commands_llm.SqlMigrateTransactionAndErrorsTests.test_sqlmigrate_returns_joined_sql_in_order
coverage json -o coverage.json
: '>>>>> End Test Output'
