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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 view_tests.tests.test_debug_llm.BadListTests._make_bad_list view_tests.tests.test_debug_llm.BadListTests.setUp view_tests.tests.test_debug_llm.BadListTests.test_custom_list_subclass_cleanses_deeply_nested_structures view_tests.tests.test_debug_llm.BadListTests.test_custom_list_subclass_cleanses_inner_tuple_contents view_tests.tests.test_debug_llm.BadListTests.test_custom_list_subclass_cleanses_nested_dicts view_tests.tests.test_debug_llm.BadListTests.test_custom_list_subclass_does_not_evaluate_callables view_tests.tests.test_debug_llm.BadListTests.test_custom_list_subclass_preserves_inner_tuple_types view_tests.tests.test_debug_llm.BadListTests.test_custom_list_subclass_recurses_in_list_of_lists view_tests.tests.test_debug_llm.BadListTests.test_custom_list_subclass_with_multiple_sensitive_entries view_tests.tests.test_debug_llm.BadListTests.test_custom_list_subclass_with_sensitive_inner_dict_is_cleansed view_tests.tests.test_debug_llm.BadListTests.test_custom_list_subclass_wraps_callable_element
coverage json -o coverage.json
: '>>>>> End Test Output'
