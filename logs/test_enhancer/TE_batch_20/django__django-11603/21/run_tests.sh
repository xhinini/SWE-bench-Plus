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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 aggregation.tests_llm.DistinctAggregateTests.setUpTestData aggregation.tests_llm.DistinctAggregateTests.test_aggregate_with_named_alias_and_distinct aggregation.tests_llm.DistinctAggregateTests.test_annotate_with_avg_distinct_does_not_raise aggregation.tests_llm.DistinctAggregateTests.test_avg_allows_distinct_aggregate aggregation.tests_llm.DistinctAggregateTests.test_avg_distinct_duration_field aggregation.tests_llm.DistinctAggregateTests.test_min_disallow_distinct_raises aggregation.tests_llm.DistinctAggregateTests.test_repr_contains_distinct_for_avg aggregation.tests_llm.DistinctAggregateTests.test_repr_contains_distinct_for_sum aggregation.tests_llm.DistinctAggregateTests.test_sum_allows_distinct_aggregate aggregation.tests_llm.DistinctAggregateTests.test_sum_distinct_on_related_field aggregation.tests_llm.DistinctAggregateTests.test_values_aggregate_with_avg_distinct
coverage json -o coverage.json
: '>>>>> End Test Output'
