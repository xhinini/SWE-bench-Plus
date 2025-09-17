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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_commands_llm.SQLMigrateTransactionTests.test_default_db_backwards_no_transaction_if_non_transactional migrations.test_commands_llm.SQLMigrateTransactionTests.test_default_db_backwards_shows_transaction_if_transactional migrations.test_commands_llm.SQLMigrateTransactionTests.test_default_db_forward_no_transaction_if_non_transactional migrations.test_commands_llm.SQLMigrateTransactionTests.test_default_db_forward_shows_transaction_if_transactional migrations.test_commands_llm.SQLMigrateTransactionTests.test_non_atomic_migration_does_not_show_transactions_even_if_db_supports migrations.test_commands_llm.SQLMigrateTransactionTests.test_non_atomic_migration_other_db_does_not_show_transactions_even_if_db_supports migrations.test_commands_llm.SQLMigrateTransactionTests.test_other_db_backwards_no_transaction_if_non_transactional migrations.test_commands_llm.SQLMigrateTransactionTests.test_other_db_forward_no_transaction_if_non_transactional migrations.test_commands_llm.SQLMigrateTransactionTests.test_other_db_forward_shows_transaction_if_transactional migrations.test_commands_llm.SQLMigrateTransactionTests.test_transaction_wrappers_ordering_when_present_on_other_db
coverage json -o coverage.json
: '>>>>> End Test Output'
