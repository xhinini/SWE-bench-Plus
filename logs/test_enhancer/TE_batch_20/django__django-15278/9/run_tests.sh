#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.test_add_field_primary_key_after_rows_sqlite schema.tests_llm.test_add_field_primary_key_autofield_sqlite schema.tests_llm.test_add_field_primary_key_bigautofield_sqlite schema.tests_llm.test_add_field_primary_key_bigintegerfield_sqlite schema.tests_llm.test_add_field_primary_key_charfield_sqlite schema.tests_llm.test_add_field_primary_key_integerfield_sqlite schema.tests_llm.test_add_field_primary_key_many_variations_sqlite schema.tests_llm.test_add_field_primary_key_one_to_onefield_sqlite schema.tests_llm.test_add_field_primary_key_with_nullable_sqlite
coverage json -o coverage.json
: '>>>>> End Test Output'
