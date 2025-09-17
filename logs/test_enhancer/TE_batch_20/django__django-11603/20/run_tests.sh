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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 aggregation.tests_llm.DistinctAggregateRegressionTests.test_avg_allows_distinct_in_aggregate aggregation.tests_llm.DistinctAggregateRegressionTests.test_avg_distinct_with_case_when aggregation.tests_llm.DistinctAggregateRegressionTests.test_avg_distinct_works_in_arithmetic_expression aggregation.tests_llm.DistinctAggregateRegressionTests.test_sum_allows_distinct_in_aggregate aggregation.tests_llm.DistinctAggregateRegressionTests.test_sum_distinct_with_custom_alias aggregation.tests_llm.DistinctAggregateRegressionTests.test_sum_distinct_with_duration_field aggregation.tests_llm.DistinctAggregateRegressionTests.test_sum_distinct_with_values_and_aggregate
coverage json -o coverage.json
: '>>>>> End Test Output'
