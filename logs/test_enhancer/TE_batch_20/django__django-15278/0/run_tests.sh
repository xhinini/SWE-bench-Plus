#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.SqliteAddFieldPrimaryKeyTests._column_exists schema.tests_llm.SqliteAddFieldPrimaryKeyTests.test_add_field_autofield_primary_key schema.tests_llm.SqliteAddFieldPrimaryKeyTests.test_add_field_bigautofield_primary_key schema.tests_llm.SqliteAddFieldPrimaryKeyTests.test_add_field_biginteger_primary_key schema.tests_llm.SqliteAddFieldPrimaryKeyTests.test_add_field_charfield_primary_key schema.tests_llm.SqliteAddFieldPrimaryKeyTests.test_add_field_decimal_primary_key schema.tests_llm.SqliteAddFieldPrimaryKeyTests.test_add_field_integer_primary_key schema.tests_llm.SqliteAddFieldPrimaryKeyTests.test_add_field_slugfield_primary_key schema.tests_llm.SqliteAddFieldPrimaryKeyTests.test_add_field_smallautofield_primary_key schema.tests_llm.SqliteAddFieldPrimaryKeyTests.test_add_field_smallinteger_primary_key schema.tests_llm.SqliteAddFieldPrimaryKeyTests.test_add_field_uuidfield_primary_key
coverage json -o coverage.json
: '>>>>> End Test Output'
