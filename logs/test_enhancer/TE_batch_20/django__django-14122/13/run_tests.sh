#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 ordering.tests_llm.GroupByExactSQLTests.setUpTestData ordering.tests_llm.GroupByMetaOrderingTests.assert_group_by_does_not_contain ordering.tests_llm.GroupByMetaOrderingTests.setUpTestData ordering.tests_llm.GroupByMetaOrderingTests.test_distinct_with_values_and_annotate ordering.tests_llm.GroupByMetaOrderingTests.test_group_by_on_child_model_with_meta_ordering_in_parent ordering.tests_llm.GroupByMetaOrderingTests.test_group_by_pub_date_with_f_expression_in_meta_ordering_model ordering.tests_llm.GroupByMetaOrderingTests.test_group_by_values_and_ordering_with_annotation_constant ordering.tests_llm.GroupByMetaOrderingTests.test_group_by_with_values_and_filtering ordering.tests_llm.GroupByMetaOrderingTests.test_group_by_with_values_and_ordering_not_specified ordering.tests_llm.GroupByMetaOrderingTests.test_values_group_by_pub_date_not_affected_by_meta_ordering
coverage json -o coverage.json
: '>>>>> End Test Output'
