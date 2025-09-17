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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 aggregation.tests_llm.DistinctAggregateRegressionTests.setUpTestData aggregation.tests_llm.DistinctAggregateRegressionTests.test_attempt_distinct_on_non_distinct_aggregate_raises aggregation.tests_llm.DistinctAggregateRegressionTests.test_avg_allows_distinct_in_aggregate aggregation.tests_llm.DistinctAggregateRegressionTests.test_avg_allows_distinct_in_annotate aggregation.tests_llm.DistinctAggregateRegressionTests.test_avg_distinct_in_values_aggregate aggregation.tests_llm.DistinctAggregateRegressionTests.test_count_star_with_filter_raises_valueerror aggregation.tests_llm.DistinctAggregateRegressionTests.test_custom_aggregate_disallows_distinct aggregation.tests_llm.DistinctAggregateRegressionTests.test_get_repr_options_contains_distinct_flag aggregation.tests_llm.DistinctAggregateRegressionTests.test_sum_allows_distinct_in_aggregate aggregation.tests_llm.DistinctAggregateRegressionTests.test_sum_allows_distinct_in_annotate aggregation.tests_llm.DistinctAggregateRegressionTests.test_sum_distinct_matches_python_distinct_sum_of_prices
coverage json -o coverage.json
: '>>>>> End Test Output'
