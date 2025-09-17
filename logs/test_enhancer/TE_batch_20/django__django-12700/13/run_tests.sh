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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 view_tests.tests.test_debug_llm.SafeExceptionReporterFilterRegressionTests.test_callable_inside_list_subclass_is_wrapped_and_no_error view_tests.tests.test_debug_llm.SafeExceptionReporterFilterRegressionTests.test_cleanse_setting_with_list_subclass_nested_in_dict view_tests.tests.test_debug_llm.SafeExceptionReporterFilterRegressionTests.test_cleanse_setting_with_list_subclass_nested_in_list view_tests.tests.test_debug_llm.SafeExceptionReporterFilterRegressionTests.test_cleanse_setting_with_list_subclass_returns_builtin_list view_tests.tests.test_debug_llm.SafeExceptionReporterFilterRegressionTests.test_cleanse_setting_with_tuple_subclass_nested_in_dict view_tests.tests.test_debug_llm.SafeExceptionReporterFilterRegressionTests.test_cleanse_setting_with_tuple_subclass_nested_in_list view_tests.tests.test_debug_llm.SafeExceptionReporterFilterRegressionTests.test_cleanse_setting_with_tuple_subclass_returns_builtin_tuple view_tests.tests.test_debug_llm.SafeExceptionReporterFilterRegressionTests.test_get_safe_settings_handles_list_subclass_setting view_tests.tests.test_debug_llm.SafeExceptionReporterFilterRegressionTests.test_get_safe_settings_handles_tuple_subclass_setting
coverage json -o coverage.json
: '>>>>> End Test Output'
