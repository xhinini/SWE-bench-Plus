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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 aggregation.tests_llm.test_aggregate_query_with_avg_distinct_runs_and_returns_expected_value aggregation.tests_llm.test_aggregate_query_with_sum_distinct_runs_and_returns_expected_value aggregation.tests_llm.test_annotate_with_avg_distinct_per_row aggregation.tests_llm.test_annotate_with_sum_distinct_per_row aggregation.tests_llm.test_avg_class_allows_distinct_flag aggregation.tests_llm.test_avg_distinct_appears_in_executed_sql aggregation.tests_llm.test_avg_instantiation_with_distinct_does_not_raise_and_has_option aggregation.tests_llm.test_sum_class_allows_distinct_flag aggregation.tests_llm.test_sum_distinct_appears_in_executed_sql aggregation.tests_llm.test_sum_instantiation_with_distinct_does_not_raise_and_has_option
coverage json -o coverage.json
: '>>>>> End Test Output'
