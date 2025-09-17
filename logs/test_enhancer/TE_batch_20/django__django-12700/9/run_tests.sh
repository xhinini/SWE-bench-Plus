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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 view_tests.tests.test_debug_llm.CleanseSettingNonStringKeyTests.setUp view_tests.tests.test_debug_llm.CleanseSettingNonStringKeyTests.test_deeply_nested_structures_with_non_string_key_all_sensitive_values_redacted view_tests.tests.test_debug_llm.CleanseSettingNonStringKeyTests.test_list_of_callables_with_non_string_key_gets_wrapped view_tests.tests.test_debug_llm.CleanseSettingNonStringKeyTests.test_list_of_dicts_with_non_string_key_is_recursed_and_sensitive_values_redacted view_tests.tests.test_debug_llm.CleanseSettingNonStringKeyTests.test_list_with_non_string_key_and_tuple_inner_elements view_tests.tests.test_debug_llm.CleanseSettingNonStringKeyTests.test_list_with_none_and_sensitive_dicts_and_non_string_key view_tests.tests.test_debug_llm.CleanseSettingNonStringKeyTests.test_mixed_list_tuple_dicts_with_non_string_key_are_all_recursed view_tests.tests.test_debug_llm.CleanseSettingNonStringKeyTests.test_nested_empty_structures_with_non_string_key_and_sensitive_inner_dicts view_tests.tests.test_debug_llm.CleanseSettingNonStringKeyTests.test_preserves_original_sequence_types_when_key_is_non_string view_tests.tests.test_debug_llm.CleanseSettingNonStringKeyTests.test_tuple_of_callables_with_non_string_key_gets_wrapped view_tests.tests.test_debug_llm.CleanseSettingNonStringKeyTests.test_tuple_of_dicts_with_non_string_key_is_recursed_and_sensitive_values_redacted
coverage json -o coverage.json
: '>>>>> End Test Output'
