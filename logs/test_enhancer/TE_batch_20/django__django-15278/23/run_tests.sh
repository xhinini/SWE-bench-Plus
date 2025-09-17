#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.test_add_field_primary_key_big_integer_calls_remake schema.tests_llm.test_add_field_primary_key_bigautofield_calls_remake schema.tests_llm.test_add_field_primary_key_binaryfield_calls_remake schema.tests_llm.test_add_field_primary_key_char_calls_remake schema.tests_llm.test_add_field_primary_key_integer_calls_remake schema.tests_llm.test_add_field_primary_key_one_to_one_calls_remake schema.tests_llm.test_add_field_primary_key_slug_calls_remake schema.tests_llm.test_add_field_primary_key_smallautofield_calls_remake schema.tests_llm.test_add_field_primary_key_uuid_calls_remake
coverage json -o coverage.json
: '>>>>> End Test Output'
