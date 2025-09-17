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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 aggregation.tests_llm.DistinctFormattingTests.test_count_distinct_aggregate_sql_contains_space aggregation.tests_llm.DistinctFormattingTests.test_count_distinct_annotation_query_str_contains_space aggregation.tests_llm.DistinctFormattingTests.test_count_distinct_in_values_aggregate_contains_space aggregation.tests_llm.DistinctFormattingTests.test_count_distinct_multiple_aggregates_sql_contains_space_multiple_times aggregation.tests_llm.DistinctFormattingTests.test_count_distinct_on_related_field_contains_space aggregation.tests_llm.DistinctFormattingTests.test_count_distinct_star_query_str_contains_space aggregation.tests_llm.DistinctFormattingTests.test_count_distinct_values_annotate_query_str_contains_space aggregation.tests_llm.DistinctFormattingTests.test_count_distinct_with_case_in_aggregate_sql_contains_space aggregation.tests_llm.DistinctFormattingTests.test_count_distinct_with_expression_argument_contains_space aggregation.tests_llm.DistinctFormattingTests.test_count_distinct_with_output_field_query_str_contains_space
coverage json -o coverage.json
: '>>>>> End Test Output'
