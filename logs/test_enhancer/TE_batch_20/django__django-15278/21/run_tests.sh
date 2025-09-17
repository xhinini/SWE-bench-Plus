#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.test_add_field_primary_key_autofield_triggers_remake schema.tests_llm.test_add_field_primary_key_bigautofield_triggers_remake schema.tests_llm.test_add_field_primary_key_clears_deferred_sql schema.tests_llm.test_add_field_primary_key_fk_triggers_remake schema.tests_llm.test_add_field_primary_key_integerfield_triggers_remake schema.tests_llm.test_add_field_primary_key_onetoonefield_triggers_remake schema.tests_llm.test_add_field_primary_key_preserves_data schema.tests_llm.test_add_field_primary_key_smallautofield_triggers_remake schema.tests_llm.test_add_field_primary_key_uuidfield_triggers_remake
coverage json -o coverage.json
: '>>>>> End Test Output'
