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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 aggregation.tests_llm.test_annotate_avg_distinct_on_related_field aggregation.tests_llm.test_annotate_sum_distinct_on_related_field aggregation.tests_llm.test_annotate_then_aggregate_with_distinct aggregation.tests_llm.test_avg_distinct_aggregate_returns_expected_value aggregation.tests_llm.test_avg_distinct_duration_field aggregation.tests_llm.test_avg_distinct_sql_contains_distinct aggregation.tests_llm.test_get_repr_options_includes_distinct_flag aggregation.tests_llm.test_sum_distinct_aggregate_returns_expected_value aggregation.tests_llm.test_sum_distinct_duration_field aggregation.tests_llm.test_sum_distinct_sql_contains_distinct
coverage json -o coverage.json
: '>>>>> End Test Output'
