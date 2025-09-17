#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_bulk_update_llm.BulkUpdateCustomExpressionTests.test_datetimefield_custom_expression queries.test_bulk_update_llm.BulkUpdateCustomExpressionTests.test_jsonfield_custom_expression queries.test_bulk_update_llm.CustomExpression.__init__ queries.test_bulk_update_llm.CustomExpression.resolve_expression
coverage json -o coverage.json
: '>>>>> End Test Output'
