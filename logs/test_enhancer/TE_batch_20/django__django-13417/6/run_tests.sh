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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.tests_llm.QuerySetOrderedGroupByRegressionTests.setUpTestData queries.tests_llm.QuerySetOrderedGroupByRegressionTests.test_annotate_then_explicit_order_by_remains_ordered queries.tests_llm.QuerySetOrderedGroupByRegressionTests.test_annotate_with_aggregate_sets_group_by_and_unorders queries.tests_llm.QuerySetOrderedGroupByRegressionTests.test_chain_clone_group_by_independence queries.tests_llm.QuerySetOrderedGroupByRegressionTests.test_distinct_query_with_manual_group_by_not_ordered queries.tests_llm.QuerySetOrderedGroupByRegressionTests.test_manual_group_by_flag_hides_default_ordering queries.tests_llm.QuerySetOrderedGroupByRegressionTests.test_order_by_cleared_then_annotate_still_not_ordered queries.tests_llm.QuerySetOrderedGroupByRegressionTests.test_related_model_default_ordering_hidden_by_aggregate queries.tests_llm.QuerySetOrderedGroupByRegressionTests.test_values_list_then_annotate_is_not_ordered_when_grouped queries.tests_llm.QuerySetOrderedGroupByRegressionTests.test_values_parent_with_aggregate_not_ordered queries.tests_llm.QuerySetOrderedGroupByRegressionTests.test_values_then_annotate_is_not_ordered_when_grouped
coverage json -o coverage.json
: '>>>>> End Test Output'
