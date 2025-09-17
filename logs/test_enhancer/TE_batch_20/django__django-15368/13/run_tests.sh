#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_bulk_update_llm.BulkUpdateExpressionLikeTests.test_custom_expr_json_field queries.test_bulk_update_llm.BulkUpdateExpressionLikeTests.test_without_resolve_is_treated_as_literal queries.test_bulk_update_llm.CustomExpr.__init__ queries.test_bulk_update_llm.CustomExpr.resolve_expression queries.test_bulk_update_llm.WithoutResolve.__init__ queries.test_bulk_update_llm.WithoutResolve.__str__
coverage json -o coverage.json
: '>>>>> End Test Output'
