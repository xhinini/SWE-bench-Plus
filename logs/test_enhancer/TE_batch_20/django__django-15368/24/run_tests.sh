#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_bulk_update_llm.BulkUpdateCustomExpressionTests.setUp queries.test_bulk_update_llm.__repr__'] (queries.test_bulk_update_llm.BulkUpdateCustomExpressionTests.['_ExprProxy.__init__', '_ExprProxy.resolve_expression', '_ExprProxy)
coverage json -o coverage.json
: '>>>>> End Test Output'
