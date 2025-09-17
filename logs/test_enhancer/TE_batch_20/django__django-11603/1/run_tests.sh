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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 aggregation.tests_llm.DistinctAggregateTests.setUpTestData aggregation.tests_llm.DistinctAggregateTests.test_avg_distinct_in_aggregate_returns_expected_value aggregation.tests_llm.DistinctAggregateTests.test_avg_distinct_in_annotate_works aggregation.tests_llm.DistinctAggregateTests.test_avg_instantiation_allows_distinct aggregation.tests_llm.DistinctAggregateTests.test_count_distinct_in_aggregate_returns_expected_value aggregation.tests_llm.DistinctAggregateTests.test_repr_options_include_distinct_for_avg aggregation.tests_llm.DistinctAggregateTests.test_repr_options_include_distinct_for_sum aggregation.tests_llm.DistinctAggregateTests.test_sum_distinct_in_aggregate_returns_expected_value aggregation.tests_llm.DistinctAggregateTests.test_sum_distinct_in_annotate_works aggregation.tests_llm.DistinctAggregateTests.test_sum_instantiation_allows_distinct aggregation.tests_llm.DistinctAggregateTests.test_using_distinct_on_aggregate_subclass_not_allowing_it_raises
coverage json -o coverage.json
: '>>>>> End Test Output'
