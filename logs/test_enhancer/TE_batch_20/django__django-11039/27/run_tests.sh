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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_commands_llm.SqlMigrateTransactionBehaviorTests.test_command_output_transaction_reflects_db_support migrations.test_commands_llm.SqlMigrateTransactionBehaviorTests.test_sqlmigrate_backwards_start_transaction_sql_empty_default_db migrations.test_commands_llm.SqlMigrateTransactionBehaviorTests.test_sqlmigrate_other_db_non_transactional_backwards migrations.test_commands_llm.SqlMigrateTransactionBehaviorTests.test_sqlmigrate_start_transaction_sql_empty_no_wrapper_default_db
coverage json -o coverage.json
: '>>>>> End Test Output'
