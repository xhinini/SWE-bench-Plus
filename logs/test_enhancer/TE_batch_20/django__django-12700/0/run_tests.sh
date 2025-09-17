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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 view_tests.tests.test_debug_llm.RegressionCleanseListTupleTests.test_cleanse_does_not_invoke_callables_inside_list view_tests.tests.test_debug_llm.RegressionCleanseListTupleTests.test_cleanse_setting_with_list_subclass_direct view_tests.tests.test_debug_llm.RegressionCleanseListTupleTests.test_cleanse_setting_with_list_subclass_via_get_safe_settings view_tests.tests.test_debug_llm.RegressionCleanseListTupleTests.test_cleanse_setting_with_tuple_subclass_direct view_tests.tests.test_debug_llm.RegressionCleanseListTupleTests.test_cleanse_setting_with_tuple_subclass_via_get_safe_settings
coverage json -o coverage.json
: '>>>>> End Test Output'
