#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.test_add_field_primary_key_autofield_triggers_remake schema.tests_llm.test_add_field_primary_key_bigautofield_triggers_remake schema.tests_llm.test_add_field_primary_key_bigintegerfield_triggers_remake schema.tests_llm.test_add_field_primary_key_charfield_triggers_remake schema.tests_llm.test_add_field_primary_key_decimalfield_triggers_remake schema.tests_llm.test_add_field_primary_key_integerfield_triggers_remake schema.tests_llm.test_add_field_primary_key_positiveintegerfield_triggers_remake schema.tests_llm.test_add_field_primary_key_slugfield_triggers_remake schema.tests_llm.test_add_field_primary_key_smallautofield_triggers_remake schema.tests_llm.test_add_field_primary_key_uuidfield_triggers_remake
coverage json -o coverage.json
: '>>>>> End Test Output'
