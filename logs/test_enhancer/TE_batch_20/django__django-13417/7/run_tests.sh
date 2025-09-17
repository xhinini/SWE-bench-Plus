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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.tests_llm.QuerySetGroupByOrderedTests.setUpTestData queries.tests_llm.QuerySetGroupByOrderedTests.test_annotate_order_by_cleared_ordering_false queries.tests_llm.QuerySetGroupByOrderedTests.test_annotate_then_explicit_order_by_overrides_default queries.tests_llm.QuerySetGroupByOrderedTests.test_annotate_triggers_group_by_and_ordered_false queries.tests_llm.QuerySetGroupByOrderedTests.test_annotate_with_extra_order_by_true queries.tests_llm.QuerySetGroupByOrderedTests.test_default_ordering_respected_when_not_group_by queries.tests_llm.QuerySetGroupByOrderedTests.test_distinct_with_aggregate_group_by_ordered_false queries.tests_llm.QuerySetGroupByOrderedTests.test_ranking_annotate_group_by_ordered_false queries.tests_llm.QuerySetGroupByOrderedTests.test_values_annotate_group_by_ordered_false queries.tests_llm.QuerySetGroupByOrderedTests.test_values_annotate_then_explicit_order_by_overrides_default queries.tests_llm.QuerySetGroupByOrderedTests.test_values_list_with_annotate_group_by_ordered_false
coverage json -o coverage.json
: '>>>>> End Test Output'
