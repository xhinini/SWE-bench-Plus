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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_commands_llm.SqlMigrateTransactionRegressionTests.test_sqlmigrate_backwards_non_atomic_even_if_db_supports migrations.test_commands_llm.SqlMigrateTransactionRegressionTests.test_sqlmigrate_backwards_non_transactional_db_no_wrappers migrations.test_commands_llm.SqlMigrateTransactionRegressionTests.test_sqlmigrate_backwards_transactional_db_with_wrappers migrations.test_commands_llm.SqlMigrateTransactionRegressionTests.test_sqlmigrate_forwards_non_transactional_db_no_wrappers migrations.test_commands_llm.SqlMigrateTransactionRegressionTests.test_sqlmigrate_forwards_transactional_db_with_wrappers migrations.test_commands_llm.SqlMigrateTransactionRegressionTests.test_sqlmigrate_no_transaction_when_migration_non_atomic_even_if_db_supports migrations.test_commands_llm.SqlMigrateTransactionRegressionTests.test_sqlmigrate_other_database_backwards_respects_can_rollback_ddl migrations.test_commands_llm.SqlMigrateTransactionRegressionTests.test_sqlmigrate_other_database_respects_can_rollback_ddl migrations.test_commands_llm.SqlMigrateTransactionRegressionTests.test_sqlmigrate_transaction_wrappers_positioning_backwards
coverage json -o coverage.json
: '>>>>> End Test Output'
