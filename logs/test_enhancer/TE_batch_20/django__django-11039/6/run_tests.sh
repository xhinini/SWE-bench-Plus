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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_commands_llm.test_sqlmigrate_backwards_no_transaction_when_db_cannot_rollback_ddl_default migrations.test_commands_llm.test_sqlmigrate_backwards_no_transaction_when_db_cannot_rollback_ddl_other_db migrations.test_commands_llm.test_sqlmigrate_forwards_no_transaction_when_db_cannot_rollback_ddl_default migrations.test_commands_llm.test_sqlmigrate_forwards_no_transaction_when_db_cannot_rollback_ddl_other_db migrations.test_commands_llm.test_sqlmigrate_no_color_forced_even_if_supports_color_true migrations.test_commands_llm.test_sqlmigrate_no_end_when_end_sql_empty migrations.test_commands_llm.test_sqlmigrate_no_start_when_start_sql_empty migrations.test_commands_llm.test_sqlmigrate_non_atomic_never_shows_transaction_wrappers_even_if_db_supports migrations.test_commands_llm.test_sqlmigrate_shows_wrappers_only_when_atomic_and_db_supports_for_other_db
coverage json -o coverage.json
: '>>>>> End Test Output'
