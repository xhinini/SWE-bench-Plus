#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_bulk_update_llm.BulkUpdateDuckExpressionTests.setUpTestData queries.test_bulk_update_llm.BulkUpdateDuckExpressionTests.test_duck_expression_inherited_fields queries.test_bulk_update_llm.BulkUpdateDuckExpressionTests.test_duck_expression_with_function_wrapper queries.test_bulk_update_llm.BulkUpdateDuckExpressionTests.test_duck_expression_with_multiple_fields queries.test_bulk_update_llm.ConstExpr.__init__ queries.test_bulk_update_llm.ConstExpr.resolve_expression queries.test_bulk_update_llm.ExprWrapper.__init__ queries.test_bulk_update_llm.ExprWrapper.resolve_expression queries.test_bulk_update_llm.IncExpr.__init__ queries.test_bulk_update_llm.IncExpr.resolve_expression
coverage json -o coverage.json
: '>>>>> End Test Output'
