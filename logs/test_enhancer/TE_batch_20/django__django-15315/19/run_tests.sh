#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.FieldHashImmutabilityTests.test_dict_key_after_contribute_to_class model_fields.tests_llm.FieldHashImmutabilityTests.test_hash_unchanged_on_meta_name_change model_fields.tests_llm.FieldHashImmutabilityTests.test_hash_unchanged_when_used_in_set_and_meta_changed model_fields.tests_llm.FieldHashImmutabilityTests.test_set_membership_after_contribute_to_class
coverage json -o coverage.json
: '>>>>> End Test Output'
