#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.AddPrimaryKeyFieldSQLiteTests._remove_id_and_add_field schema.tests_llm.AddPrimaryKeyFieldSQLiteTests.tearDown schema.tests_llm.AddPrimaryKeyFieldSQLiteTests.test_add_autofield_primary_key_when_db_column_differs schema.tests_llm.AddPrimaryKeyFieldSQLiteTests.test_add_bigautofield_primary_key schema.tests_llm.AddPrimaryKeyFieldSQLiteTests.test_add_bigintegerfield_primary_key schema.tests_llm.AddPrimaryKeyFieldSQLiteTests.test_add_charfield_primary_key schema.tests_llm.AddPrimaryKeyFieldSQLiteTests.test_add_integerfield_primary_key schema.tests_llm.AddPrimaryKeyFieldSQLiteTests.test_add_positiveintegerfield_primary_key schema.tests_llm.AddPrimaryKeyFieldSQLiteTests.test_add_slugfield_primary_key schema.tests_llm.AddPrimaryKeyFieldSQLiteTests.test_add_smallautofield_primary_key schema.tests_llm.AddPrimaryKeyFieldSQLiteTests.test_add_uuidfield_primary_key
coverage json -o coverage.json
: '>>>>> End Test Output'
