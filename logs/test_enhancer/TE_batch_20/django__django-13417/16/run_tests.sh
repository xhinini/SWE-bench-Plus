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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.tests_llm.QuerySetGroupByOrderedTests.setUpTestData queries.tests_llm.QuerySetGroupByOrderedTests.test_alias_with_aggregate_is_not_ordered queries.tests_llm.QuerySetGroupByOrderedTests.test_annotate_then_explicit_order_marks_ordered queries.tests_llm.QuerySetGroupByOrderedTests.test_annotate_with_aggregate_is_not_ordered queries.tests_llm.QuerySetGroupByOrderedTests.test_distinct_values_with_aggregate_is_not_ordered queries.tests_llm.QuerySetGroupByOrderedTests.test_multiple_annotations_with_one_aggregate_is_not_ordered queries.tests_llm.QuerySetGroupByOrderedTests.test_ranking_model_annotate_with_aggregate_is_not_ordered queries.tests_llm.QuerySetGroupByOrderedTests.test_related_field_aggregation_is_not_ordered queries.tests_llm.QuerySetGroupByOrderedTests.test_values_list_then_annotate_with_aggregate_is_not_ordered queries.tests_llm.QuerySetGroupByOrderedTests.test_values_then_annotate_then_order_marks_ordered queries.tests_llm.QuerySetGroupByOrderedTests.test_values_then_annotate_with_aggregate_is_not_ordered
coverage json -o coverage.json
: '>>>>> End Test Output'
