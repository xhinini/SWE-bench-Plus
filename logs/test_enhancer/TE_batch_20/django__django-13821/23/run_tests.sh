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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.tests_llm.CheckSQLiteVersionExtraTests._reload_base_module backends.sqlite.tests_llm.CheckSQLiteVersionExtraTests.test_above_3_9_does_not_raise backends.sqlite.tests_llm.CheckSQLiteVersionExtraTests.test_below_3_9_raises backends.sqlite.tests_llm.CheckSQLiteVersionExtraTests.test_equal_3_8_3_raises backends.sqlite.tests_llm.CheckSQLiteVersionExtraTests.test_equal_3_9_0_does_not_raise backends.sqlite.tests_llm.CheckSQLiteVersionExtraTests.test_error_message_contains_reported_version backends.sqlite.tests_llm.CheckSQLiteVersionExtraTests.test_long_tuple_3_9_0_1_does_not_raise backends.sqlite.tests_llm.CheckSQLiteVersionExtraTests.test_major_only_tuple_raises backends.sqlite.tests_llm.CheckSQLiteVersionExtraTests.test_module_reload_without_side_effect_after_ok backends.sqlite.tests_llm.CheckSQLiteVersionExtraTests.test_reload_reflects_patched_values_sequence backends.sqlite.tests_llm.CheckSQLiteVersionExtraTests.test_short_tuple_3_9_only_raises
coverage json -o coverage.json
: '>>>>> End Test Output'
