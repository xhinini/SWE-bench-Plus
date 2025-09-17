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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 aggregation.tests_llm.test_annotate_then_aggregate_preserves_distinct_spacing aggregation.tests_llm.test_count_distinct_in_grouped_values_has_space aggregation.tests_llm.test_count_distinct_in_values_aggregate_has_space aggregation.tests_llm.test_count_distinct_in_values_list_annotation_has_space aggregation.tests_llm.test_count_distinct_sql_in_aggregate_has_space aggregation.tests_llm.test_count_distinct_sql_in_annotate_has_space aggregation.tests_llm.test_count_distinct_with_case_expression_sql_has_space aggregation.tests_llm.test_count_star_distinct_sql_has_space aggregation.tests_llm.test_distinct_count_on_related_field_has_space aggregation.tests_llm.test_multiple_counts_one_distinct_renders_space
coverage json -o coverage.json
: '>>>>> End Test Output'
