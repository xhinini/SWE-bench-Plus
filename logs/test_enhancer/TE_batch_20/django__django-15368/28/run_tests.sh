#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_bulk_update_llm.BulkUpdateCustomExpressionTests.setUp queries.test_bulk_update_llm.BulkUpdateCustomExpressionTests.test_custom_expression_returned_rows_with_batching_and_duplicates queries.test_bulk_update_llm.CustomInc.__init__ queries.test_bulk_update_llm.CustomInc.__repr__ queries.test_bulk_update_llm.CustomInc.resolve_expression queries.test_bulk_update_llm.CustomIncCast.__init__ queries.test_bulk_update_llm.CustomIncCast.__repr__ queries.test_bulk_update_llm.CustomIncCast.resolve_expression
coverage json -o coverage.json
: '>>>>> End Test Output'
