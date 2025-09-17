#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.test_add_nullable_binaryfield_sqlite schema.tests_llm.test_add_nullable_booleanfield_sqlite schema.tests_llm.test_add_nullable_charfield_sqlite schema.tests_llm.test_add_nullable_datetimefield_sqlite schema.tests_llm.test_add_nullable_floatfield_sqlite schema.tests_llm.test_add_nullable_integer_field_sqlite schema.tests_llm.test_add_nullable_textfield_sqlite schema.tests_llm.test_add_o2o_field_nullable_sqlite schema.tests_llm.test_add_primary_key_field_rebuilds_table_sqlite schema.tests_llm.test_add_unique_field_rebuilds_table_sqlite
coverage json -o coverage.json
: '>>>>> End Test Output'
