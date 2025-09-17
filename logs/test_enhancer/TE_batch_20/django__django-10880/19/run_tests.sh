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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 aggregation.tests_llm.test_sql_annotate_values_list_count_distinct_has_space aggregation.tests_llm.test_sql_count_distinct_in_aggregate_has_space aggregation.tests_llm.test_sql_count_distinct_in_annotation_query_string_has_space aggregation.tests_llm.test_sql_count_distinct_in_complex_query_has_space aggregation.tests_llm.test_sql_count_distinct_named_alias_in_aggregate_has_space aggregation.tests_llm.test_sql_count_distinct_star_has_space aggregation.tests_llm.test_sql_count_distinct_with_case_expression_has_space aggregation.tests_llm.test_sql_multiple_aggregates_one_distinct_only_has_single_distinct_token aggregation.tests_llm.test_sql_non_distinct_has_no_distinct_token aggregation.tests_llm.test_sql_values_aggregate_count_distinct_has_space
coverage json -o coverage.json
: '>>>>> End Test Output'
