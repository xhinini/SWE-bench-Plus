#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.SQLiteAddFieldPrimaryKeyTests._assert_add_field_remakes_table schema.tests_llm.SQLiteAddFieldPrimaryKeyTests.test_add_field_primary_key_bigautofield schema.tests_llm.SQLiteAddFieldPrimaryKeyTests.test_add_field_primary_key_charfield schema.tests_llm.SQLiteAddFieldPrimaryKeyTests.test_add_field_primary_key_datetimefield schema.tests_llm.SQLiteAddFieldPrimaryKeyTests.test_add_field_primary_key_decimalfield schema.tests_llm.SQLiteAddFieldPrimaryKeyTests.test_add_field_primary_key_foreignkey schema.tests_llm.SQLiteAddFieldPrimaryKeyTests.test_add_field_primary_key_integerfield schema.tests_llm.SQLiteAddFieldPrimaryKeyTests.test_add_field_primary_key_onetoone schema.tests_llm.SQLiteAddFieldPrimaryKeyTests.test_add_field_primary_key_slugfield schema.tests_llm.SQLiteAddFieldPrimaryKeyTests.test_add_field_primary_key_uuidfield
coverage json -o coverage.json
: '>>>>> End Test Output'
