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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 aggregation.tests_llm.test_avg_allows_distinct_in_aggregate aggregation.tests_llm.test_avg_distinct_get_repr_options_includes_distinct aggregation.tests_llm.test_avg_distinct_in_annotation aggregation.tests_llm.test_avg_distinct_with_case_expression aggregation.tests_llm.test_avg_distinct_with_filter_kwarg aggregation.tests_llm.test_distinct_appears_in_generated_sql_for_aggregates aggregation.tests_llm.test_sum_allows_distinct_in_aggregate aggregation.tests_llm.test_sum_distinct_over_m2m aggregation.tests_llm.test_sum_distinct_values_groupby aggregation.tests_llm.test_sum_distinct_with_output_field_decimal
coverage json -o coverage.json
: '>>>>> End Test Output'
