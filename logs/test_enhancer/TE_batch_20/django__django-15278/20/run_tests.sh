#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 schema.tests_llm.test_add_field_does_not_access_one_to_one_on_plain_field schema.tests_llm.test_add_field_effective_default_triggers_remake schema.tests_llm.test_add_field_missing_one_to_one_attribute_on_real_field_does_not_raise schema.tests_llm.test_add_field_not_null_triggers_remake schema.tests_llm.test_add_field_nullable_without_default_does_not_remake schema.tests_llm.test_add_field_one_to_one_real_field_triggers_remake schema.tests_llm.test_add_field_primary_key_triggers_remake schema.tests_llm.test_add_field_unique_triggers_remake schema.tests_llm.test_add_field_with_real_field_delegates_for_nullable_field
coverage json -o coverage.json
: '>>>>> End Test Output'
