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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_commands_llm.test_sqlmigrate_database_backwards_non_transactional migrations.test_commands_llm.test_sqlmigrate_database_backwards_transactional migrations.test_commands_llm.test_sqlmigrate_handles_empty_end_sql migrations.test_commands_llm.test_sqlmigrate_handles_empty_start_sql migrations.test_commands_llm.test_sqlmigrate_output_transaction_state_is_per_call migrations.test_commands_llm.test_sqlmigrate_respects_can_rollback_default_db migrations.test_commands_llm.test_sqlmigrate_respects_database_option_non_transactional migrations.test_commands_llm.test_sqlmigrate_respects_database_option_over_default_features migrations.test_commands_llm.test_sqlmigrate_respects_database_option_transactional
coverage json -o coverage.json
: '>>>>> End Test Output'
