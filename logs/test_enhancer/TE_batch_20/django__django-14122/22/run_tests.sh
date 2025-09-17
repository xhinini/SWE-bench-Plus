#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 ordering.tests_llm.GroupByRegressionTests._group_by_columns_from_sql ordering.tests_llm.GroupByRegressionTests.setUpTestData ordering.tests_llm.GroupByRegressionTests.test_annotate_then_values_group_by_sql ordering.tests_llm.GroupByRegressionTests.test_values_author_and_id_group_by_sql ordering.tests_llm.GroupByRegressionTests.test_values_author_annotate_last_date_group_by_sql ordering.tests_llm.GroupByRegressionTests.test_values_author_distinct_group_by_sql ordering.tests_llm.GroupByRegressionTests.test_values_author_group_by_sql_no_meta_columns ordering.tests_llm.GroupByRegressionTests.test_values_author_multiple_annotations_group_by_sql ordering.tests_llm.GroupByRegressionTests.test_values_author_order_by_headline_group_by_sql ordering.tests_llm.GroupByRegressionTests.test_values_author_order_by_upper_expression_group_by_sql ordering.tests_llm.GroupByRegressionTests.test_values_with_explicit_ordering_cleared_group_by_sql
coverage json -o coverage.json
: '>>>>> End Test Output'
