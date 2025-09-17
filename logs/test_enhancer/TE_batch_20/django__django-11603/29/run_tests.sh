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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 aggregation.tests_llm.test_aggregate_filter_clause_not_used_when_unsupported aggregation.tests_llm.test_aggregate_filter_clause_used_when_supported aggregation.tests_llm.test_avg_and_sum_distinct_aggregate_on_price aggregation.tests_llm.test_avg_distinct_aggregate_value_and_sql_contains_distinct aggregation.tests_llm.test_avg_distinct_annotation_query_contains_distinct aggregation.tests_llm.test_count_star_with_filter_raises_value_error aggregation.tests_llm.test_repr_options_contains_distinct_for_avg_and_sum aggregation.tests_llm.test_sum_distinct_aggregate_value_and_sql_contains_distinct aggregation.tests_llm.test_sum_distinct_annotation_query_contains_distinct aggregation.tests_llm.test_sum_distinct_in_values_annotation_runs
coverage json -o coverage.json
: '>>>>> End Test Output'
