#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.HashStabilityTests.test_field_dict_key_after_model_assignment_and_removal model_fields.tests_llm.HashStabilityTests.test_field_in_set_after_manual_model_change model_fields.tests_llm.HashStabilityTests.test_hash_stable_when_setting_model_manually model_fields.tests_llm.HashStabilityTests.test_hash_unchanged_after_contribute_to_class model_fields.tests_llm.HashStabilityTests.test_set_membership_preserved_after_contribute
coverage json -o coverage.json
: '>>>>> End Test Output'
