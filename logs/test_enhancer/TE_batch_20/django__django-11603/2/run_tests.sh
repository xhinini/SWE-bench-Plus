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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 aggregation.tests_llm.test_avg_allows_distinct_and_sql_includes_distinct aggregation.tests_llm.test_avg_distinct_in_values_annotate_does_not_raise aggregation.tests_llm.test_avg_with_case_expression_and_distinct aggregation.tests_llm.test_get_repr_options_includes_distinct_for_avg aggregation.tests_llm.test_get_repr_options_includes_distinct_for_sum aggregation.tests_llm.test_sum_allows_distinct_and_sql_includes_distinct aggregation.tests_llm.test_sum_distinct_duration_field aggregation.tests_llm.test_sum_distinct_prices_per_publisher_annotation aggregation.tests_llm.test_sum_distinct_publisher_awards_value aggregation.tests_llm.test_sum_distinct_with_output_field_duration_works
coverage json -o coverage.json
: '>>>>> End Test Output'
