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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.tests_llm.CheckSQLiteVersionReloadTests.reload_base backends.sqlite.tests_llm.CheckSQLiteVersionReloadTests.test_long_tuple_is_handled backends.sqlite.tests_llm.CheckSQLiteVersionReloadTests.test_major_version_lower_raises backends.sqlite.tests_llm.CheckSQLiteVersionReloadTests.test_message_contains_actual_sqlite_version backends.sqlite.tests_llm.CheckSQLiteVersionReloadTests.test_minor_version_lower_raises backends.sqlite.tests_llm.CheckSQLiteVersionReloadTests.test_no_error_for_just_above_boundary backends.sqlite.tests_llm.CheckSQLiteVersionReloadTests.test_short_tuple_like_ backends.sqlite.tests_llm.CheckSQLiteVersionReloadTests.test_version_3_8_3_raises backends.sqlite.tests_llm.CheckSQLiteVersionReloadTests.test_version_above_3_9_0_does_not_raise backends.sqlite.tests_llm.CheckSQLiteVersionReloadTests.test_version_below_3_9_0_raises backends.sqlite.tests_llm.CheckSQLiteVersionReloadTests.test_version_equal_3_9_0_does_not_raise
coverage json -o coverage.json
: '>>>>> End Test Output'
