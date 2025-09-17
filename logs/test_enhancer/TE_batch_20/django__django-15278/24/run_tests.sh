#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.test_add_field_triggers_remake_for_primary_key_autofield schema.tests_llm.test_add_field_triggers_remake_for_primary_key_bigautofield schema.tests_llm.test_add_field_triggers_remake_for_primary_key_bigintegerfield schema.tests_llm.test_add_field_triggers_remake_for_primary_key_charfield schema.tests_llm.test_add_field_triggers_remake_for_primary_key_integerfield schema.tests_llm.test_add_field_triggers_remake_for_primary_key_positiveintegerfield schema.tests_llm.test_add_field_triggers_remake_for_primary_key_slugfield schema.tests_llm.test_add_field_triggers_remake_for_primary_key_smallautofield schema.tests_llm.test_add_field_triggers_remake_for_primary_key_smallintegerfield schema.tests_llm.test_add_field_triggers_remake_for_primary_key_uuidfield
coverage json -o coverage.json
: '>>>>> End Test Output'
