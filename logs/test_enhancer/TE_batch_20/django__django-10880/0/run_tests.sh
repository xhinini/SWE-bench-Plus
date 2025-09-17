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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 aggregation.tests_llm.test__get_repr_options_includes_distinct_and_filter_keys aggregation.tests_llm.test_aggregate_with_filter_backend_supports_filter_clause_includes_distinct_and_filter aggregation.tests_llm.test_aggregate_with_filter_backend_without_filter_clause_uses_case_and_includes_distinct aggregation.tests_llm.test_annotate_count_distinct_sql_contains_space aggregation.tests_llm.test_count_distinct_on_related_field_sql_contains_space aggregation.tests_llm.test_count_distinct_sql_contains_space aggregation.tests_llm.test_count_distinct_with_case_expression_sql_contains_space aggregation.tests_llm.test_count_without_distinct_does_not_include_distinct aggregation.tests_llm.test_multiple_aggregates_one_distinct_and_one_non_distinct aggregation.tests_llm.test_values_annotate_count_distinct_sql_contains_space
coverage json -o coverage.json
: '>>>>> End Test Output'
