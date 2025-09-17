#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_bulk_update_llm.BulkUpdateExpressionLikeTests.test_expression_like_and_none_values queries.test_bulk_update_llm.BulkUpdateExpressionLikeTests.test_mixed_none_and_expression_like_with_duplicates_and_batching queries.test_bulk_update_llm.ExpressionLike.__init__ queries.test_bulk_update_llm.ExpressionLike.__repr__ queries.test_bulk_update_llm.ExpressionLike.resolve_expression
coverage json -o coverage.json
: '>>>>> End Test Output'
