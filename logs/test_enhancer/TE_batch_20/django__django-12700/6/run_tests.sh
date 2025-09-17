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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 view_tests.tests.test_debug_llm.CleanseListTupleRegressionTests.setUp view_tests.tests.test_debug_llm.CleanseListTupleRegressionTests.test_cleanse_empty_list view_tests.tests.test_debug_llm.CleanseListTupleRegressionTests.test_cleanse_empty_tuple view_tests.tests.test_debug_llm.CleanseListTupleRegressionTests.test_cleanse_list_of_callables_wrapped view_tests.tests.test_debug_llm.CleanseListTupleRegressionTests.test_cleanse_list_with_none_and_dicts view_tests.tests.test_debug_llm.CleanseListTupleRegressionTests.test_cleanse_nested_empty_structures view_tests.tests.test_debug_llm.CleanseListTupleRegressionTests.test_cleanse_tuple_mixed_types_preserve_type view_tests.tests.test_debug_llm.CleanseListTupleRegressionTests.test_cleanse_tuple_of_tuples_and_lists view_tests.tests.test_debug_llm.CleanseListTupleRegressionTests.test_deeply_nested_structures view_tests.tests.test_debug_llm.CleanseListTupleRegressionTests.test_get_safe_settings_handles_list_and_tuple_settings
coverage json -o coverage.json
: '>>>>> End Test Output'
