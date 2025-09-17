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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.tests_llm.QuerySetOrderedGroupByTests.setUpTestData queries.tests_llm.QuerySetOrderedGroupByTests.test_aggregate_annotation_sets_group_by_and_ordered_false queries.tests_llm.QuerySetOrderedGroupByTests.test_aggregate_then_explicit_order_by_keeps_ordered_true queries.tests_llm.QuerySetOrderedGroupByTests.test_annotate_values_then_order_by_keeps_ordered_true queries.tests_llm.QuerySetOrderedGroupByTests.test_default_ordering_ignored_when_group_by_true queries.tests_llm.QuerySetOrderedGroupByTests.test_distinct_query_with_manual_group_by_reports_unordered_when_default queries.tests_llm.QuerySetOrderedGroupByTests.test_extra_order_by_overrides_group_by queries.tests_llm.QuerySetOrderedGroupByTests.test_manual_group_by_does_not_affect_explicit_ordering queries.tests_llm.QuerySetOrderedGroupByTests.test_multiple_annotations_with_and_without_aggregate queries.tests_llm.QuerySetOrderedGroupByTests.test_none_queryset_remains_ordered queries.tests_llm.QuerySetOrderedGroupByTests.test_values_with_aggregate_sets_group_by_and_ordered_false
coverage json -o coverage.json
: '>>>>> End Test Output'
