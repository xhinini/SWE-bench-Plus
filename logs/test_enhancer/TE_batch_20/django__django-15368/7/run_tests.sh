#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_bulk_update_llm.BulkUpdateDuckTypingTests.test_duck_expression_json_field queries.test_bulk_update_llm.DuckField.__init__ queries.test_bulk_update_llm.DuckField.resolve_expression queries.test_bulk_update_llm.DuckIncr.__init__ queries.test_bulk_update_llm.DuckIncr.resolve_expression queries.test_bulk_update_llm.DuckValue.__init__ queries.test_bulk_update_llm.DuckValue.resolve_expression
coverage json -o coverage.json
: '>>>>> End Test Output'
