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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.tests_llm.GroupByOrderedTests.setUpTestData queries.tests_llm.GroupByOrderedTests.test_annotate_then_values_group_by_ignores_default_ordering queries.tests_llm.GroupByOrderedTests.test_distinct_values_annotate_group_by_ignores_default_ordering queries.tests_llm.GroupByOrderedTests.test_extra_order_by_overrides_group_by queries.tests_llm.GroupByOrderedTests.test_group_by_on_model_without_default_ordering queries.tests_llm.GroupByOrderedTests.test_group_by_on_other_model_with_default_ordering_ignored queries.tests_llm.GroupByOrderedTests.test_group_by_with_annotation_order_by_annotation_sets_ordered_true queries.tests_llm.GroupByOrderedTests.test_none_queryset_group_by_ignores_default_ordering queries.tests_llm.GroupByOrderedTests.test_order_by_clears_then_group_by_ignores_default queries.tests_llm.GroupByOrderedTests.test_order_by_overrides_group_by queries.tests_llm.GroupByOrderedTests.test_values_annotate_group_by_ignores_default_ordering
coverage json -o coverage.json
: '>>>>> End Test Output'
