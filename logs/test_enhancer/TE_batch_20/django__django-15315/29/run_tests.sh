#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.FieldHashStabilityTests.test_field_key_in_dict_survives_contribute_to_class model_fields.tests_llm.FieldHashStabilityTests.test_field_membership_in_collections_after_multiple_mutations model_fields.tests_llm.FieldHashStabilityTests.test_field_membership_in_set_survives_contribute_to_class model_fields.tests_llm.FieldHashStabilityTests.test_hash_unchanged_after_changing_app_label model_fields.tests_llm.FieldHashStabilityTests.test_hash_unchanged_after_changing_model_name model_fields.tests_llm.FieldHashStabilityTests.test_hash_unchanged_after_detach_model_attribute model_fields.tests_llm.FieldHashStabilityTests.test_hash_unchanged_on_contribute_to_class model_fields.tests_llm.FieldHashStabilityTests.test_set_membership_survives_meta_changes
coverage json -o coverage.json
: '>>>>> End Test Output'
