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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 view_tests.tests.test_debug_llm.CleanseSettingListTupleTests.setUp view_tests.tests.test_debug_llm.CleanseSettingListTupleTests.test_empty_list view_tests.tests.test_debug_llm.CleanseSettingListTupleTests.test_empty_tuple view_tests.tests.test_debug_llm.CleanseSettingListTupleTests.test_get_safe_settings_integration_with_non_str_key view_tests.tests.test_debug_llm.CleanseSettingListTupleTests.test_list_in_dict_with_non_str_key_is_cleansed view_tests.tests.test_debug_llm.CleanseSettingListTupleTests.test_list_with_none_and_sensitive_dict view_tests.tests.test_debug_llm.CleanseSettingListTupleTests.test_nested_empty_structures view_tests.tests.test_debug_llm.CleanseSettingListTupleTests.test_nested_list_of_dicts view_tests.tests.test_debug_llm.CleanseSettingListTupleTests.test_top_level_tuple_setting_masks_inner_sensitive view_tests.tests.test_debug_llm.CleanseSettingListTupleTests.test_tuple_in_dict_with_non_str_key_is_cleansed view_tests.tests.test_debug_llm.CleanseSettingListTupleTests.test_tuple_with_mixed_types
coverage json -o coverage.json
: '>>>>> End Test Output'
