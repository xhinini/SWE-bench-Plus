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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_commands_llm.SQLMigrateTransactionTests.test_command_output_transaction_false_when_db_no_support_even_if_atomic migrations.test_commands_llm.SQLMigrateTransactionTests.test_command_output_transaction_set_based_on_db_features_and_migration_atomic_true migrations.test_commands_llm.SQLMigrateTransactionTests.test_sqlmigrate_backward_excludes_wrappers_when_db_no_rollback migrations.test_commands_llm.SQLMigrateTransactionTests.test_sqlmigrate_backward_includes_wrappers_when_atomic_and_db_supports migrations.test_commands_llm.SQLMigrateTransactionTests.test_sqlmigrate_excludes_wrappers_when_db_no_rollback_forward migrations.test_commands_llm.SQLMigrateTransactionTests.test_sqlmigrate_excludes_wrappers_when_migration_non_atomic_even_if_db_supports_forward migrations.test_commands_llm.SQLMigrateTransactionTests.test_sqlmigrate_handles_start_sql_none_no_wrappers migrations.test_commands_llm.SQLMigrateTransactionTests.test_sqlmigrate_includes_wrappers_when_atomic_and_db_supports_forward migrations.test_commands_llm.SQLMigrateTransactionTests.test_sqlmigrate_no_start_sql_defined_no_wrappers migrations.test_commands_llm.SQLMigrateTransactionTests.test_sqlmigrate_respects_database_option_transaction_wrappers
coverage json -o coverage.json
: '>>>>> End Test Output'
