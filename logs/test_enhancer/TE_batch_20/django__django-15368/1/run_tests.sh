#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_bulk_update_llm.BulkUpdateRegressionTests.setUpTestData queries.test_bulk_update_llm.BulkUpdateRegressionTests.test_bulk_update_multiple_objects_with_mixed_expressions queries.test_bulk_update_llm.BulkUpdateRegressionTests.test_bulk_update_with_functions_and_expressions queries.test_bulk_update_llm.BulkUpdateRegressionTests.test_custom_expr_on_json_field queries.test_bulk_update_llm.BulkUpdateRegressionTests.test_custom_expression_like_object_updates_charfield queries.test_bulk_update_llm.BulkUpdateRegressionTests.test_custom_expression_returning_F_expression
coverage json -o coverage.json
: '>>>>> End Test Output'
