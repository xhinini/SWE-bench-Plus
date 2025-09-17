#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.test_add_nullable_binary_field_does_not_remake_or_raise schema.tests_llm.test_add_nullable_char_field_does_not_remake_or_raise schema.tests_llm.test_add_nullable_datetime_field_does_not_remake_or_raise schema.tests_llm.test_add_nullable_integer_field_does_not_remake_or_raise schema.tests_llm.test_add_primary_key_autofield_remakes_table schema.tests_llm.test_add_primary_key_bigint_field_remakes_table schema.tests_llm.test_add_primary_key_integer_field_remakes_table schema.tests_llm.test_add_primary_key_uuidfield_remakes_table schema.tests_llm.test_adding_nullable_field_does_not_access_one_to_one_attribute
coverage json -o coverage.json
: '>>>>> End Test Output'
