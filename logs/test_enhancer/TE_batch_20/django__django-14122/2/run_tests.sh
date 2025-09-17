#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 ordering.tests_llm.GroupByRegressionTests._group_by_fragment ordering.tests_llm.GroupByRegressionTests.setUpTestData ordering.tests_llm.GroupByRegressionTests.test_order_by_annotation_constant_is_not_added_to_group_by ordering.tests_llm.GroupByRegressionTests.test_order_by_annotation_is_not_added_to_group_by ordering.tests_llm.GroupByRegressionTests.test_ordering_by_grouped_column_does_not_duplicate_group_entry
coverage json -o coverage.json
: '>>>>> End Test Output'
