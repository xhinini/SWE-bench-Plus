#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_bulk_update_llm.BulkUpdateExprLikeTests.setUp queries.test_bulk_update_llm.BulkUpdateExprLikeTests.test_object_without_resolve_is_wrapped_and_saved queries.test_bulk_update_llm.resolve_expression'] (queries.test_bulk_update_llm.BulkUpdateExprLikeTests.['ExprLike.__init__', 'ExprLike) queries.test_bulk_update_llm.resolve_expression'] (queries.test_bulk_update_llm.BulkUpdateExprLikeTests.['ExprLikeToF.__init__', 'ExprLikeToF)
coverage json -o coverage.json
: '>>>>> End Test Output'
