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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 aggregation.tests_llm.test_aggregate_default_alias_with_distinct aggregation.tests_llm.test_avg_allows_distinct_in_aggregate_and_sql aggregation.tests_llm.test_avg_and_sum_repr_options_and_copy_preserve_distinct aggregation.tests_llm.test_constructing_avg_and_sum_with_distinct_does_not_raise aggregation.tests_llm.test_count_allows_distinct_and_sql aggregation.tests_llm.test_max_raises_on_distinct aggregation.tests_llm.test_stddev_raises_on_distinct aggregation.tests_llm.test_sum_allows_distinct_in_aggregate_and_sql aggregation.tests_llm.test_sum_distinct_matches_manual_distinct_sum aggregation.tests_llm.test_variance_raises_on_distinct
coverage json -o coverage.json
: '>>>>> End Test Output'
