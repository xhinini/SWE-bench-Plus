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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 aggregation.tests_llm.DistinctSQLRegressionTests.test_aggregate_in_subquery_sql_has_space aggregation.tests_llm.DistinctSQLRegressionTests.test_annotate_distinct_count_str_query_has_space aggregation.tests_llm.DistinctSQLRegressionTests.test_case_expression_distinct_sql_has_space aggregation.tests_llm.DistinctSQLRegressionTests.test_count_distinct_on_related_field_has_space aggregation.tests_llm.DistinctSQLRegressionTests.test_count_distinct_sql_has_space aggregation.tests_llm.DistinctSQLRegressionTests.test_multiple_distinct_aggregates_sql_has_space aggregation.tests_llm.DistinctSQLRegressionTests.test_no_distinct_followed_immediately_by_parenthesis_in_any_query aggregation.tests_llm.DistinctSQLRegressionTests.test_sum_distinct_sql_has_space aggregation.tests_llm.DistinctSQLRegressionTests.test_values_aggregate_distinct_sql_has_space aggregation.tests_llm.DistinctSQLRegressionTests.test_values_annotation_with_distinct_in_group_by_sql_has_space
coverage json -o coverage.json
: '>>>>> End Test Output'
