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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 aggregation.tests_llm.DistinctAggregateRegressionTests.setUpTestData aggregation.tests_llm.DistinctAggregateRegressionTests.test_annotate_with_distinct_avg_evaluates aggregation.tests_llm.DistinctAggregateRegressionTests.test_avg_allows_distinct_in_aggregate aggregation.tests_llm.DistinctAggregateRegressionTests.test_avg_default_alias_with_distinct aggregation.tests_llm.DistinctAggregateRegressionTests.test_avg_distinct_generates_DISTINCT_in_sql aggregation.tests_llm.DistinctAggregateRegressionTests.test_avg_repr_options_include_distinct aggregation.tests_llm.DistinctAggregateRegressionTests.test_count_distinct_consistency aggregation.tests_llm.DistinctAggregateRegressionTests.test_sum_allows_distinct_in_aggregate aggregation.tests_llm.DistinctAggregateRegressionTests.test_sum_default_alias_with_distinct aggregation.tests_llm.DistinctAggregateRegressionTests.test_sum_distinct_generates_DISTINCT_in_sql aggregation.tests_llm.DistinctAggregateRegressionTests.test_sum_repr_options_include_distinct
coverage json -o coverage.json
: '>>>>> End Test Output'
