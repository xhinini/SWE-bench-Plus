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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_commands_llm.SqlMigrateOutputTransactionTests._make_executor migrations.test_commands_llm.SqlMigrateOutputTransactionTests._run_and_get_output migrations.test_commands_llm.SqlMigrateOutputTransactionTests.test_atomic_and_non_transactional_db_no_wrappers migrations.test_commands_llm.SqlMigrateOutputTransactionTests.test_atomic_and_transactional_db_adds_wrappers migrations.test_commands_llm.SqlMigrateOutputTransactionTests.test_atomic_non_transactional_db_backwards_no_wrappers migrations.test_commands_llm.SqlMigrateOutputTransactionTests.test_atomic_non_transactional_other_db_no_wrappers migrations.test_commands_llm.SqlMigrateOutputTransactionTests.test_atomic_transactional_db_backwards_adds_wrappers migrations.test_commands_llm.SqlMigrateOutputTransactionTests.test_atomic_transactional_other_db_adds_wrappers migrations.test_commands_llm.SqlMigrateOutputTransactionTests.test_non_atomic_and_non_transactional_db_no_wrappers migrations.test_commands_llm.SqlMigrateOutputTransactionTests.test_non_atomic_but_transactional_db_no_wrappers migrations.test_commands_llm.SqlMigrateOutputTransactionTests.test_non_atomic_non_transactional_db_backwards_no_wrappers migrations.test_commands_llm.SqlMigrateOutputTransactionTests.test_non_atomic_transactional_db_backwards_no_wrappers
coverage json -o coverage.json
: '>>>>> End Test Output'
