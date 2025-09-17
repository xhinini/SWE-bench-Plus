#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_bulk_update_llm.BulkUpdateExpressionLikeTests.setUp queries.test_bulk_update_llm.BulkUpdateExpressionLikeTests.test_bulk_update_custom_pk_and_expression_like_field queries.test_bulk_update_llm.BulkUpdateExpressionLikeTests.test_bulk_update_preserves_falsey_pk_and_expression_like queries.test_bulk_update_llm.BulkUpdateExpressionLikeTests.test_bulk_update_with_mixture_of_expression_like_and_none queries.test_bulk_update_llm.DummyExprReturningAdd.__init__ queries.test_bulk_update_llm.DummyExprReturningAdd.__repr__ queries.test_bulk_update_llm.DummyExprReturningAdd.resolve_expression queries.test_bulk_update_llm.DummyExprReturningF.__init__ queries.test_bulk_update_llm.DummyExprReturningF.__repr__ queries.test_bulk_update_llm.DummyExprReturningF.resolve_expression
coverage json -o coverage.json
: '>>>>> End Test Output'
