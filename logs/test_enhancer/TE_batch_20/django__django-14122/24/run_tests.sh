#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 ordering.tests_llm.GroupByRegressionTests._group_by_clause_upper ordering.tests_llm.GroupByRegressionTests.setUpTestData ordering.tests_llm.GroupByRegressionTests.test_child_model_order_by_ptr_field_with_meta_ordering_group_by_ok ordering.tests_llm.GroupByRegressionTests.test_extra_order_by_does_not_leak_meta_ordering_into_group_by ordering.tests_llm.GroupByRegressionTests.test_function_ordering_ignored_in_group_by_when_meta_ordering ordering.tests_llm.GroupByRegressionTests.test_order_by_f_expression_ignored_in_group_by_when_meta_ordering ordering.tests_llm.GroupByRegressionTests.test_rawsql_order_by_table_column_ignored_in_group_by
coverage json -o coverage.json
: '>>>>> End Test Output'
