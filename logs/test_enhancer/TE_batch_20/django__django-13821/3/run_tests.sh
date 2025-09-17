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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.tests_llm.CheckSQLiteVersionReloadTests.reload_under_version backends.sqlite.tests_llm.CheckSQLiteVersionReloadTests.test_exact_old_threshold_3_8_3_raises backends.sqlite.tests_llm.CheckSQLiteVersionReloadTests.test_import_time_check_triggers_on_reload backends.sqlite.tests_llm.CheckSQLiteVersionReloadTests.test_just_below_threshold_3_8_4_raises backends.sqlite.tests_llm.CheckSQLiteVersionReloadTests.test_message_includes_actual_database_string backends.sqlite.tests_llm.CheckSQLiteVersionReloadTests.test_older_minor_version_raises backends.sqlite.tests_llm.CheckSQLiteVersionReloadTests.test_short_tuple_like_3_9_raises
coverage json -o coverage.json
: '>>>>> End Test Output'
