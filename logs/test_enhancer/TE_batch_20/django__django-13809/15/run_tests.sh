#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.test_check_called_and_migrations_run_when_not_skipped admin_scripts.tests_llm.test_check_migrations_called_before_run_when_not_skipped admin_scripts.tests_llm.test_check_migrations_called_before_run_when_skipped_flag_true admin_scripts.tests_llm.test_check_migrations_called_with_skip_checks_false admin_scripts.tests_llm.test_check_migrations_called_with_skip_checks_true admin_scripts.tests_llm.test_check_skipped_but_migrations_run admin_scripts.tests_llm.test_migration_message_present_when_migrations_indicate_work admin_scripts.tests_llm.test_no_skipping_message_with_skip_checks_true admin_scripts.tests_llm.test_performing_message_with_skip_checks_false
coverage json -o coverage.json
: '>>>>> End Test Output'
