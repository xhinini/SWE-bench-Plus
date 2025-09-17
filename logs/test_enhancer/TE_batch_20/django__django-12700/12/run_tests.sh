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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 view_tests.tests.test_debug_llm.CleanseListTupleRegressionTests.setUp view_tests.tests.test_debug_llm.CleanseListTupleRegressionTests.test_callable_in_weird_list_wrapped view_tests.tests.test_debug_llm.CleanseListTupleRegressionTests.test_callable_in_weird_tuple_wrapped view_tests.tests.test_debug_llm.CleanseListTupleRegressionTests.test_complex_weird_nested_combo_masks_secret view_tests.tests.test_debug_llm.CleanseListTupleRegressionTests.test_custom_list_subclass_masks_secret view_tests.tests.test_debug_llm.CleanseListTupleRegressionTests.test_custom_tuple_subclass_masks_secret view_tests.tests.test_debug_llm.CleanseListTupleRegressionTests.test_nested_weird_subclasses_masks_secret view_tests.tests.test_debug_llm.CleanseListTupleRegressionTests.test_weird_list_inside_tuple_masks_secret view_tests.tests.test_debug_llm.CleanseListTupleRegressionTests.test_weird_list_with_nested_list_masks_secret view_tests.tests.test_debug_llm.CleanseListTupleRegressionTests.test_weird_tuple_inside_list_masks_secret view_tests.tests.test_debug_llm.CleanseListTupleRegressionTests.test_weird_tuple_with_nested_tuple_masks_secret view_tests.tests.test_debug_llm.__new__'] (view_tests.tests.test_debug_llm.CleanseListTupleRegressionTests.['WeirdList) view_tests.tests.test_debug_llm.__new__'] (view_tests.tests.test_debug_llm.CleanseListTupleRegressionTests.['WeirdTuple)
coverage json -o coverage.json
: '>>>>> End Test Output'
