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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 aggregation.tests_llm.DistinctSQLTests.test_sql_distinct_space_in_aggregate_after_annotate aggregation.tests_llm.DistinctSQLTests.test_sql_distinct_space_in_aggregate_count aggregation.tests_llm.DistinctSQLTests.test_sql_distinct_space_in_annotate_count aggregation.tests_llm.DistinctSQLTests.test_sql_distinct_space_in_annotation_on_related aggregation.tests_llm.DistinctSQLTests.test_sql_distinct_space_in_grouped_values_annotate aggregation.tests_llm.DistinctSQLTests.test_sql_distinct_space_in_multiple_aggregates aggregation.tests_llm.DistinctSQLTests.test_sql_distinct_space_in_values_annotate aggregation.tests_llm.DistinctSQLTests.test_sql_distinct_space_in_values_list_annotation aggregation.tests_llm.DistinctSQLTests.test_sql_distinct_space_with_case_expression aggregation.tests_llm.DistinctSQLTests.test_sql_distinct_space_with_custom_aggregate_template
coverage json -o coverage.json
: '>>>>> End Test Output'
