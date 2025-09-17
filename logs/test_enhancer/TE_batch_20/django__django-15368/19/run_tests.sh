#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_bulk_update_llm.BulkUpdateExpressionLikeTests.setUp queries.test_bulk_update_llm.BulkUpdateExpressionLikeTests.test_expression_like_on_multiple_fields queries.test_bulk_update_llm.BulkUpdateExpressionLikeTests.test_mixed_expr_like_and_plain_multiple_batches queries.test_bulk_update_llm._ExprLike.__init__ queries.test_bulk_update_llm._ExprLike.__repr__ queries.test_bulk_update_llm._ExprLike.resolve_expression
coverage json -o coverage.json
: '>>>>> End Test Output'
