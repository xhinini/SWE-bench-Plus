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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_commands_llm.test_handle_sets_output_transaction_false_when_db_non_transactional migrations.test_commands_llm.test_handle_sets_output_transaction_true_when_both_true migrations.test_commands_llm.test_handle_uses_specified_database_connection migrations.test_commands_llm.test_sqlmigrate_for_non_atomic_migration_on_other_db migrations.test_commands_llm.test_sqlmigrate_other_db_non_transactional_backwards migrations.test_commands_llm.test_sqlmigrate_other_db_non_transactional_forwards migrations.test_commands_llm.test_sqlmigrate_other_db_transactional_backwards migrations.test_commands_llm.test_sqlmigrate_other_db_transactional_forwards
coverage json -o coverage.json
: '>>>>> End Test Output'
