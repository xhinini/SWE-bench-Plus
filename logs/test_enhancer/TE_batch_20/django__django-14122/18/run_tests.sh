#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 ordering.tests_llm.GroupByMetaOrderingRegressionTests._group_by_clause ordering.tests_llm.GroupByMetaOrderingRegressionTests.setUpTestData ordering.tests_llm.GroupByMetaOrderingRegressionTests.test_distinct_with_values_and_meta_ordering_does_not_alter_group_by ordering.tests_llm.GroupByMetaOrderingRegressionTests.test_extra_select_and_group_by_does_not_include_meta_ordering ordering.tests_llm.GroupByMetaOrderingRegressionTests.test_subquery_annotation_and_group_by_no_meta_leakage
coverage json -o coverage.json
: '>>>>> End Test Output'
