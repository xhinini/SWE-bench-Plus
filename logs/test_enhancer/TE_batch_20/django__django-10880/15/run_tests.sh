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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 aggregation.tests_llm.test_annotate_count_distinct_sql_contains_space aggregation.tests_llm.test_count_distinct_expression_sql_contains_space aggregation.tests_llm.test_count_distinct_sql_contains_space aggregation.tests_llm.test_count_distinct_with_filter_sql_contains_space aggregation.tests_llm.test_custom_aggregate_distinct_sql_has_space aggregation.tests_llm.test_custom_aggregate_distinct_with_filter_sql_has_space aggregation.tests_llm.test_distinct_internally_used_in_subquery_params_and_sql aggregation.tests_llm.test_distinct_space_present_only_once_in_query aggregation.tests_llm.test_no_distinct_token_when_distinct_false aggregation.tests_llm.test_values_annotate_aggregate_contains_distinct_space
coverage json -o coverage.json
: '>>>>> End Test Output'
