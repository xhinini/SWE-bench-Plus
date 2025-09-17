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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 view_tests.tests.test_debug_llm.CleanseSettingListTupleTests._assert_inner_call_uses_empty_key view_tests.tests.test_debug_llm.CleanseSettingListTupleTests.test_callable_inside_list_is_wrapped_and_inner_call_key_empty view_tests.tests.test_debug_llm.CleanseSettingListTupleTests.test_deeply_nested_mixed_structures_uses_empty_key_for_deep_element view_tests.tests.test_debug_llm.CleanseSettingListTupleTests.test_list_element_recursion_uses_empty_key view_tests.tests.test_debug_llm.CleanseSettingListTupleTests.test_list_element_when_element_is_dict_uses_empty_key_for_element_call view_tests.tests.test_debug_llm.CleanseSettingListTupleTests.test_list_of_tuple_nested_element_uses_empty_key view_tests.tests.test_debug_llm.CleanseSettingListTupleTests.test_many_levels_of_nesting_all_use_empty_key_for_deep_value view_tests.tests.test_debug_llm.CleanseSettingListTupleTests.test_nested_list_two_levels_uses_empty_key_for_deep_element view_tests.tests.test_debug_llm.CleanseSettingListTupleTests.test_tuple_element_recursion_uses_empty_key view_tests.tests.test_debug_llm.CleanseSettingListTupleTests.test_tuple_of_dicts_elements_use_empty_key view_tests.tests.test_debug_llm.CleanseSettingListTupleTests.test_tuple_of_list_nested_element_uses_empty_key view_tests.tests.test_debug_llm.LoggingFilter.__init__ view_tests.tests.test_debug_llm.LoggingFilter.cleanse_setting
coverage json -o coverage.json
: '>>>>> End Test Output'
