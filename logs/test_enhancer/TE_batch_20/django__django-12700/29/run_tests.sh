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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 view_tests.tests.test_debug_llm.CleanseSettingListTupleRegressionTests.test_empty_list_and_tuple_subclasses_return_builtin_collections view_tests.tests.test_debug_llm.CleanseSettingListTupleRegressionTests.test_get_safe_settings_normalizes_list_subclass_from_settings view_tests.tests.test_debug_llm.CleanseSettingListTupleRegressionTests.test_get_safe_settings_normalizes_tuple_subclass_from_settings view_tests.tests.test_debug_llm.CleanseSettingListTupleRegressionTests.test_list_subclass_of_callables_are_wrapped view_tests.tests.test_debug_llm.CleanseSettingListTupleRegressionTests.test_list_subclass_returns_builtin_list_and_cleans_inner_sensitive_keys view_tests.tests.test_debug_llm.CleanseSettingListTupleRegressionTests.test_mixed_nested_list_and_tuple_subclasses_normalize_and_cleanse view_tests.tests.test_debug_llm.CleanseSettingListTupleRegressionTests.test_nested_list_subclass_elements_cleans_all_sensitive_entries view_tests.tests.test_debug_llm.CleanseSettingListTupleRegressionTests.test_tuple_subclass_of_callables_are_wrapped_and_return_builtin_tuple view_tests.tests.test_debug_llm.CleanseSettingListTupleRegressionTests.test_tuple_subclass_returns_builtin_tuple_and_cleans_inner_sensitive_keys
coverage json -o coverage.json
: '>>>>> End Test Output'
