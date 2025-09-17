#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.FieldHashTests.test_dict_key_after_manual_model_assignment model_fields.tests_llm.FieldHashTests.test_dict_key_with_contribute model_fields.tests_llm.FieldHashTests.test_field_stays_in_set_after_deepcopy_and_attach model_fields.tests_llm.FieldHashTests.test_set_membership_after_assigning_field_to_model model_fields.tests_llm.FieldHashTests.test_set_membership_after_manual_model_assignment model_fields.tests_llm.FieldHashTests.test_set_membership_with_contribute
coverage json -o coverage.json
: '>>>>> End Test Output'
