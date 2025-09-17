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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.tests_llm.QuerySetGroupByOrderedTests.setUpTestData queries.tests_llm.QuerySetGroupByOrderedTests.test_annotate_sets_group_by_and_ignores_default_ordering queries.tests_llm.QuerySetGroupByOrderedTests.test_cleared_default_ordering_with_group_by queries.tests_llm.QuerySetGroupByOrderedTests.test_default_ordering_ignored_when_group_by_true queries.tests_llm.QuerySetGroupByOrderedTests.test_empty_queryset_is_ordered_even_if_group_by queries.tests_llm.QuerySetGroupByOrderedTests.test_extra_order_by_overrides_group_by queries.tests_llm.QuerySetGroupByOrderedTests.test_group_by_flag_precedence_for_default_ordering queries.tests_llm.QuerySetGroupByOrderedTests.test_order_by_after_group_by_restores_ordered queries.tests_llm.QuerySetGroupByOrderedTests.test_order_by_overrides_group_by queries.tests_llm.QuerySetGroupByOrderedTests.test_ordered_property_does_not_evaluate_queryset queries.tests_llm.QuerySetGroupByOrderedTests.test_values_annotate_group_by_ignored_default_ordering
coverage json -o coverage.json
: '>>>>> End Test Output'
