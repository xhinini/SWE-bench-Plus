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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 view_tests.tests.test_debug_llm.ListTupleCleanseTests.setUp view_tests.tests.test_debug_llm.ListTupleCleanseTests.test_cleanse_setting_handles_deeply_nested_empty_structures view_tests.tests.test_debug_llm.ListTupleCleanseTests.test_cleanse_setting_list_of_dicts_and_nested_collections view_tests.tests.test_debug_llm.ListTupleCleanseTests.test_cleanse_setting_list_of_primitives_remain_when_not_sensitive view_tests.tests.test_debug_llm.ListTupleCleanseTests.test_cleanse_setting_list_with_none_and_empty_structures view_tests.tests.test_debug_llm.ListTupleCleanseTests.test_cleanse_setting_mixed_nesting_list_tuple view_tests.tests.test_debug_llm.ListTupleCleanseTests.test_cleanse_setting_multilevel_list_tuple_mixture view_tests.tests.test_debug_llm.ListTupleCleanseTests.test_cleanse_setting_preserves_tuple_type_and_order view_tests.tests.test_debug_llm.ListTupleCleanseTests.test_cleanse_setting_tuple_of_dicts view_tests.tests.test_debug_llm.ListTupleCleanseTests.test_cleanse_setting_wraps_callables_in_list view_tests.tests.test_debug_llm.ListTupleCleanseTests.test_get_safe_settings_with_list_setting_preserved
coverage json -o coverage.json
: '>>>>> End Test Output'
