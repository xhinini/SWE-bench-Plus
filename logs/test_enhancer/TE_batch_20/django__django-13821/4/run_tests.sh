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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.tests_llm.CheckSqliteVersionRegressionTests.reload_module_with_fake_version backends.sqlite.tests_llm.CheckSqliteVersionRegressionTests.test_import_triggers_version_check_on_reload backends.sqlite.tests_llm.CheckSqliteVersionRegressionTests.test_message_includes_reported_version_string backends.sqlite.tests_llm.CheckSqliteVersionRegressionTests.test_older_than_3_9_raises_for_3_8_11_1 backends.sqlite.tests_llm.CheckSqliteVersionRegressionTests.test_older_than_3_9_raises_for_3_8_2 backends.sqlite.tests_llm.CheckSqliteVersionRegressionTests.test_older_than_3_9_raises_for_3_8_3 backends.sqlite.tests_llm.CheckSqliteVersionRegressionTests.test_short_tuple_3_8_11_raises backends.sqlite.tests_llm.CheckSqliteVersionRegressionTests.test_short_tuple_3_9_no_raise
coverage json -o coverage.json
: '>>>>> End Test Output'
