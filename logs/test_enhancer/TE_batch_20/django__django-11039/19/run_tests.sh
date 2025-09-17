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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_commands_llm.CommandExecuteTests.test_execute_forces_no_color_option migrations.test_commands_llm.SqlMigrateRegressionTests.test_sqlmigrate_non_atomic_migration_on_transactional_db_other migrations.test_commands_llm.SqlMigrateRegressionTests.test_sqlmigrate_output_transaction_does_not_leak_between_calls migrations.test_commands_llm.SqlMigrateRegressionTests.test_sqlmigrate_respects_database_flag_non_transactional_backwards migrations.test_commands_llm.SqlMigrateRegressionTests.test_sqlmigrate_respects_database_flag_non_transactional_forwards migrations.test_commands_llm.SqlMigrateRegressionTests.test_sqlmigrate_respects_database_flag_transactional_backwards migrations.test_commands_llm.SqlMigrateRegressionTests.test_sqlmigrate_respects_database_flag_transactional_forwards migrations.test_commands_llm.SqlMigrateRegressionTests.test_sqlmigrate_transaction_wrapper_ordering_for_specified_db migrations.test_commands_llm.SqlMigrateRegressionTests.test_sqlmigrate_uses_executor_with_specified_connection
coverage json -o coverage.json
: '>>>>> End Test Output'
