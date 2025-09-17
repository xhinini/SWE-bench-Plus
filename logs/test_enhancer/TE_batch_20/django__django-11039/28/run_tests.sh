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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_commands_llm.SqlMigrateHandleUnitTests._make_fake_executor migrations.test_commands_llm.SqlMigrateHandleUnitTests.test_handle_sets_output_transaction_false_when_atomic_but_db_not_support migrations.test_commands_llm.SqlMigrateHandleUnitTests.test_handle_sets_output_transaction_false_when_non_atomic_but_db_support migrations.test_commands_llm.SqlMigrateHandleUnitTests.test_handle_sets_output_transaction_true_when_atomic_and_db_supports migrations.test_commands_llm.SqlMigrateHandleUnitTests.test_handle_uses_specified_database_connection migrations.test_commands_llm.SqlMigrateTransactionFunctionalTests.test_sqlmigrate_default_db_atomic_and_supports_ddl_shows_wrappers migrations.test_commands_llm.SqlMigrateTransactionFunctionalTests.test_sqlmigrate_default_db_atomic_but_no_ddl_hides_wrappers migrations.test_commands_llm.SqlMigrateTransactionFunctionalTests.test_sqlmigrate_non_atomic_no_transaction_even_if_db_supports
coverage json -o coverage.json
: '>>>>> End Test Output'
