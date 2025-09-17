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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 aggregation.tests_llm.DistinctSpaceTests._assert_distinct_space_in_last_query aggregation.tests_llm.DistinctSpaceTests.test_aggregate_count_distinct_has_space aggregation.tests_llm.DistinctSpaceTests.test_aggregate_count_distinct_uppercase_check aggregation.tests_llm.DistinctSpaceTests.test_annotate_count_distinct_has_space aggregation.tests_llm.DistinctSpaceTests.test_annotate_count_distinct_order_by_triggers_sql_with_space aggregation.tests_llm.DistinctSpaceTests.test_annotate_multiple_aggregates_one_distinct_sql aggregation.tests_llm.DistinctSpaceTests.test_count_distinct_case_expression_has_space aggregation.tests_llm.DistinctSpaceTests.test_count_distinct_on_joined_field_has_space aggregation.tests_llm.DistinctSpaceTests.test_count_distinct_on_related_field_has_space aggregation.tests_llm.DistinctSpaceTests.test_values_annotate_count_distinct_sql aggregation.tests_llm.DistinctSpaceTests.test_values_list_annotate_count_distinct_sql
coverage json -o coverage.json
: '>>>>> End Test Output'
