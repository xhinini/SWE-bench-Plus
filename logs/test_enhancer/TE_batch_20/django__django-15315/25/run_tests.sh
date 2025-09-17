#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.FieldHashStabilityTests.test_field_remains_in_set_after_attach model_fields.tests_llm.FieldHashStabilityTests.test_field_used_as_key_across_model_meta_change model_fields.tests_llm.FieldHashStabilityTests.test_hash_stable_after_attaching_via_attribute_assignment model_fields.tests_llm.FieldHashStabilityTests.test_hash_stable_after_contribute_to_class_explicit model_fields.tests_llm.FieldHashStabilityTests.test_hash_unchanged_when_model_meta_mutated
coverage json -o coverage.json
: '>>>>> End Test Output'
