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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 aggregation.tests_llm.test_aggregate_count_distinct_sql aggregation.tests_llm.test_annotate_count_distinct_sql aggregation.tests_llm.test_annotate_values_list_count_distinct_sql aggregation.tests_llm.test_count_distinct_case_expression_sql aggregation.tests_llm.test_count_distinct_in_subquery_aggregate_sql aggregation.tests_llm.test_count_star_distinct_sql aggregation.tests_llm.test_distinct_in_annotation_on_related aggregation.tests_llm.test_grouped_annotation_count_distinct_sql aggregation.tests_llm.test_non_count_aggregate_rejects_distinct aggregation.tests_llm.test_values_aggregate_count_distinct_sql
coverage json -o coverage.json
: '>>>>> End Test Output'
