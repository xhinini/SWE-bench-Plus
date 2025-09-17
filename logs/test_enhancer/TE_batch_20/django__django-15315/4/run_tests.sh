#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.FieldHashTests.test_collision_with_attached_and_unattached_field model_fields.tests_llm.FieldHashTests.test_copy_preserves_hash_and_equality_when_unattached model_fields.tests_llm.FieldHashTests.test_dict_key_before_and_after_attach model_fields.tests_llm.FieldHashTests.test_dict_lookup_with_hash_collision_uses_equality model_fields.tests_llm.FieldHashTests.test_hash_consistency_after_manual_model_change model_fields.tests_llm.FieldHashTests.test_hash_of_fields_with_same_creation_counter model_fields.tests_llm.FieldHashTests.test_hash_stability_on_contribute_to_class model_fields.tests_llm.FieldHashTests.test_hash_uniqueness_between_fields model_fields.tests_llm.FieldHashTests.test_hashing_unattached_field_raises_no_error model_fields.tests_llm.FieldHashTests.test_set_membership_survives_contribute
coverage json -o coverage.json
: '>>>>> End Test Output'
