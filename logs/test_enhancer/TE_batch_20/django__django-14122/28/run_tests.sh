#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 ordering.tests_llm.GroupByMetaOrderingRegressions.setUpTestData ordering.tests_llm.GroupByMetaOrderingRegressions.test_order_by_f_expression_does_not_inject_group_by_when_meta_ordering
coverage json -o coverage.json
: '>>>>> End Test Output'
