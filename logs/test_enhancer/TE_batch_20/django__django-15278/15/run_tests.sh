#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.test_add_field_primary_key_autofield_after_remove schema.tests_llm.test_add_field_primary_key_bigautofield_after_remove schema.tests_llm.test_add_field_primary_key_biginteger_after_remove schema.tests_llm.test_add_field_primary_key_charfield_after_remove schema.tests_llm.test_add_field_primary_key_integerfield_after_remove schema.tests_llm.test_add_field_primary_key_positiveinteger_after_remove schema.tests_llm.test_add_field_primary_key_slugfield_after_remove schema.tests_llm.test_add_field_primary_key_smallautofield_after_remove schema.tests_llm.test_add_field_primary_key_uuidfield_after_remove schema.tests_llm.test_add_field_primary_key_various_types_consistency
coverage json -o coverage.json
: '>>>>> End Test Output'
