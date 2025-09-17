#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 ordering.tests_llm.OrderingTests.setUpTestData ordering.tests_llm.OrderingTests.test_annotate_then_values_preserves_grouping ordering.tests_llm.OrderingTests.test_group_by_with_filtered_subquery_and_meta_ordering ordering.tests_llm.OrderingTests.test_ordering_from_meta_with_expression_ordering_does_not_affect_group_by ordering.tests_llm.OrderingTests.test_values_author_annotate_count_unaffected_by_meta_ordering ordering.tests_llm.OrderingTests.test_values_author_annotate_max_pub_date_unaffected_by_meta_ordering ordering.tests_llm.OrderingTests.test_values_author_pub_date_together_grouping ordering.tests_llm.OrderingTests.test_values_author_then_order_by_pub_date_keeps_grouping_by_author ordering.tests_llm.OrderingTests.test_values_headline_annotate_count ordering.tests_llm.OrderingTests.test_values_with_extra_select_and_meta_ordering
coverage json -o coverage.json
: '>>>>> End Test Output'
