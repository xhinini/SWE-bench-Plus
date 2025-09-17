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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_commands_llm.SqlMigrateTransactionFlagTests._assert_wrappers_absent migrations.test_commands_llm.SqlMigrateTransactionFlagTests._assert_wrappers_present migrations.test_commands_llm.SqlMigrateTransactionFlagTests._run_sqlmigrate_with_executor migrations.test_commands_llm.SqlMigrateTransactionFlagTests.test_backwards_non_atomic_but_db_supports_hides_wrappers migrations.test_commands_llm.SqlMigrateTransactionFlagTests.test_forward_non_atomic_but_db_supports_hides_wrappers migrations.test_commands_llm.SqlMigrateTransactionFlagTests.test_other_database_atomic_but_db_does_not_support_hides_wrappers
coverage json -o coverage.json
: '>>>>> End Test Output'
