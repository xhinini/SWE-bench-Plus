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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.tests_llm.QuerySetOrderedGroupByTests.setUpTestData queries.tests_llm.QuerySetOrderedGroupByTests.test_annotated_default_ordering_ignored_with_group_by queries.tests_llm.QuerySetOrderedGroupByTests.test_annotated_with_explicit_ordering_still_ordered queries.tests_llm.QuerySetOrderedGroupByTests.test_default_ordering_ignored_when_group_by_list queries.tests_llm.QuerySetOrderedGroupByTests.test_default_ordering_ignored_when_group_by_true queries.tests_llm.QuerySetOrderedGroupByTests.test_distinct_default_ordering_ignored_when_group_by queries.tests_llm.QuerySetOrderedGroupByTests.test_empty_queryset_remains_ordered_even_if_group_by queries.tests_llm.QuerySetOrderedGroupByTests.test_explicit_ordering_not_affected_by_group_by queries.tests_llm.QuerySetOrderedGroupByTests.test_extra_order_by_not_affected_by_group_by queries.tests_llm.QuerySetOrderedGroupByTests.test_values_default_ordering_ignored queries.tests_llm.QuerySetOrderedGroupByTests.test_values_list_flat_default_ordering_ignored
coverage json -o coverage.json
: '>>>>> End Test Output'
