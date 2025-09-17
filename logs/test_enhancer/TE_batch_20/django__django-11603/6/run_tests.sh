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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 aggregation.tests_llm.DistinctAggregateTests.test_annotate_sum_distinct_runs_without_error aggregation.tests_llm.DistinctAggregateTests.test_avg_allows_distinct_and_sql_contains_distinct aggregation.tests_llm.DistinctAggregateTests.test_count_star_with_filter_raises_value_error aggregation.tests_llm.DistinctAggregateTests.test_default_alias_with_complex_expression_raises aggregation.tests_llm.DistinctAggregateTests.test_max_disallows_distinct_raises aggregation.tests_llm.DistinctAggregateTests.test_min_disallows_distinct_raises aggregation.tests_llm.DistinctAggregateTests.test_multiple_distinct_aggregates_in_single_call aggregation.tests_llm.DistinctAggregateTests.test_repr_options_includes_distinct_flag aggregation.tests_llm.DistinctAggregateTests.test_sum_allows_distinct_and_sql_contains_distinct aggregation.tests_llm.DistinctAggregateTests.test_sum_default_alias_with_single_named_expression
coverage json -o coverage.json
: '>>>>> End Test Output'
