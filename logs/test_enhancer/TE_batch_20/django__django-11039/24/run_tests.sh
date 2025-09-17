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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_commands_llm.SqlMigrateTransactionTests.test_atomic_and_db_supports_ddl_shows_transactions_default migrations.test_commands_llm.SqlMigrateTransactionTests.test_atomic_but_db_does_not_support_ddl_no_transactions_default migrations.test_commands_llm.SqlMigrateTransactionTests.test_backwards_sql_hides_transactions_when_db_no_support migrations.test_commands_llm.SqlMigrateTransactionTests.test_backwards_sql_shows_transactions_when_supported migrations.test_commands_llm.SqlMigrateTransactionTests.test_database_argument_uses_that_connection_features_false migrations.test_commands_llm.SqlMigrateTransactionTests.test_database_argument_uses_that_connection_features_true migrations.test_commands_llm.SqlMigrateTransactionTests.test_no_color_for_sqlmigrate_even_if_color_supported migrations.test_commands_llm.SqlMigrateTransactionTests.test_non_atomic_and_db_no_support_never_shows_transactions migrations.test_commands_llm.SqlMigrateTransactionTests.test_non_atomic_migration_never_shows_transactions_even_if_db_supports
coverage json -o coverage.json
: '>>>>> End Test Output'
