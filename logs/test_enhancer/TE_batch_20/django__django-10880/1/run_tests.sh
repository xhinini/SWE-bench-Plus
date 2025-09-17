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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 aggregation.tests_llm.test_aggregate_count_distinct_authors_alias_has_space aggregation.tests_llm.test_aggregate_count_distinct_has_space aggregation.tests_llm.test_aggregate_count_distinct_on_related_field_has_space aggregation.tests_llm.test_aggregate_count_distinct_with_case_expression_has_space aggregation.tests_llm.test_aggregate_count_distinct_with_f_expression_has_space aggregation.tests_llm.test_annotate_count_distinct_on_related_field_str_query_has_space aggregation.tests_llm.test_annotate_count_distinct_str_query_has_space aggregation.tests_llm.test_annotate_count_distinct_with_case_expression_str_query_has_space aggregation.tests_llm.test_annotate_count_distinct_with_f_expression_str_query_has_space aggregation.tests_llm.test_values_annotate_count_distinct_in_grouping_has_space
coverage json -o coverage.json
: '>>>>> End Test Output'
