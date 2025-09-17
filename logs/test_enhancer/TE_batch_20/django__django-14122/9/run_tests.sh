#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 ordering.tests_llm.GroupByMetaOrderingTests._group_by_fragment ordering.tests_llm.GroupByMetaOrderingTests.setUpTestData ordering.tests_llm.GroupByMetaOrderingTests.test_annotate_max_then_order_by_meta_field_no_group_by_inclusion ordering.tests_llm.GroupByMetaOrderingTests.test_distinct_with_annotate_and_meta_ordering ordering.tests_llm.GroupByMetaOrderingTests.test_having_uses_aggregate_but_meta_ordering_not_in_group_by ordering.tests_llm.GroupByMetaOrderingTests.test_values_annotate_with_f_expression_order_by_not_in_group_by ordering.tests_llm.GroupByMetaOrderingTests.test_values_annotate_with_function_order_by_not_in_group_by ordering.tests_llm.GroupByMetaOrderingTests.test_values_annotate_with_meta_ordering_no_orderby_in_group_by
coverage json -o coverage.json
: '>>>>> End Test Output'
