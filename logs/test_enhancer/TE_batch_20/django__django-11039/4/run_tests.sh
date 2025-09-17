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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_commands_llm.SQLMigrateTransactionBehaviorTests.test_non_atomic_migration_respects_db_transactional_capability_for_other_db migrations.test_commands_llm.SQLMigrateTransactionBehaviorTests.test_output_transaction_flag_default_db_when_atomic_and_non_transactional migrations.test_commands_llm.SQLMigrateTransactionBehaviorTests.test_output_transaction_flag_default_db_when_atomic_and_transactional migrations.test_commands_llm.SQLMigrateTransactionBehaviorTests.test_output_transaction_flag_other_db_non_transactional migrations.test_commands_llm.SQLMigrateTransactionBehaviorTests.test_output_transaction_flag_other_db_respected migrations.test_commands_llm.SQLMigrateTransactionBehaviorTests.test_sqlmigrate_backward_other_db_transaction_wrappers_and_ordering migrations.test_commands_llm.SQLMigrateTransactionBehaviorTests.test_sqlmigrate_default_db_no_wrappers_when_non_transactional migrations.test_commands_llm.SQLMigrateTransactionBehaviorTests.test_sqlmigrate_default_db_transaction_wrappers_present migrations.test_commands_llm.SQLMigrateTransactionBehaviorTests.test_sqlmigrate_other_db_no_wrappers_when_non_transactional migrations.test_commands_llm.SQLMigrateTransactionBehaviorTests.test_sqlmigrate_other_db_transaction_wrappers_present
coverage json -o coverage.json
: '>>>>> End Test Output'
