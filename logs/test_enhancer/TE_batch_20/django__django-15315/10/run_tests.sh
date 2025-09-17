#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.FieldHashStabilityTests.test_dict_key_survives_model_meta_app_label_change model_fields.tests_llm.FieldHashStabilityTests.test_dict_key_survives_model_meta_model_name_change model_fields.tests_llm.FieldHashStabilityTests.test_frozenset_membership_preserved_after_contribute_to_class model_fields.tests_llm.FieldHashStabilityTests.test_manual_model_assignment_after_being_dict_key_does_not_invalidate_hash model_fields.tests_llm.FieldHashStabilityTests.test_set_membership_preserved_after_contribute_to_class model_fields.tests_llm.FieldHashStabilityTests.test_set_membership_survives_model_meta_model_name_change
coverage json -o coverage.json
: '>>>>> End Test Output'
