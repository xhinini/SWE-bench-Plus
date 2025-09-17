#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 ordering.tests_llm.GroupByRegressionTests._group_by_clause ordering.tests_llm.GroupByRegressionTests.setUpTestData ordering.tests_llm.GroupByRegressionTests.test_order_by_annotation_added_to_group_by
coverage json -o coverage.json
: '>>>>> End Test Output'
