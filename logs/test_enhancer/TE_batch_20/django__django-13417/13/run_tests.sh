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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.tests_llm.GroupByOrderedTests.test_alias_non_aggregate_does_not_set_group_by_and_preserves_default_ordering queries.tests_llm.GroupByOrderedTests.test_alias_with_aggregate_sets_group_by_and_ignores_default_ordering queries.tests_llm.GroupByOrderedTests.test_annotate_group_by_but_explicit_order_by_still_reports_ordered queries.tests_llm.GroupByOrderedTests.test_annotate_group_by_but_extra_order_by_still_reports_ordered queries.tests_llm.GroupByOrderedTests.test_annotate_with_aggregate_sets_group_by_and_ignores_default_ordering queries.tests_llm.GroupByOrderedTests.test_different_model_with_default_ordering_and_aggregate queries.tests_llm.GroupByOrderedTests.test_non_aggregate_annotation_does_not_set_group_by_and_preserves_default_ordering queries.tests_llm.GroupByOrderedTests.test_values_list_then_annotate_with_aggregate_sets_group_by_and_ignores_default_ordering queries.tests_llm.GroupByOrderedTests.test_values_then_annotate_group_by_but_explicit_order_by_reports_ordered queries.tests_llm.GroupByOrderedTests.test_values_then_annotate_with_aggregate_sets_group_by_and_ignores_default_ordering
coverage json -o coverage.json
: '>>>>> End Test Output'
