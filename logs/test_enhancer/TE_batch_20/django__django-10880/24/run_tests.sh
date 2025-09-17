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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 aggregation.tests_llm.test_count_distinct_absent_when_not_distinct aggregation.tests_llm.test_count_distinct_filter_on_other_field_maintains_space aggregation.tests_llm.test_count_distinct_has_space_simple_aggregate aggregation.tests_llm.test_count_distinct_in_annotate_sql aggregation.tests_llm.test_count_distinct_in_values_annotate_sql aggregation.tests_llm.test_count_distinct_with_case_expression_sql aggregation.tests_llm.test_count_distinct_with_combined_expressions_has_space aggregation.tests_llm.test_count_distinct_with_filter_sql_contains_space aggregation.tests_llm.test_count_star_distinct_has_space aggregation.tests_llm.test_multiple_count_distincts_each_has_space
coverage json -o coverage.json
: '>>>>> End Test Output'
