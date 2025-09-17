#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 invalid_models_tests.test_models_llm.ReverseRelatedIdentityTests.setUp invalid_models_tests.test_models_llm.ReverseRelatedIdentityTests.test_hash_difference_none_vs_empty_through_fields invalid_models_tests.test_models_llm.ReverseRelatedIdentityTests.test_identity_element_type_for_empty_through_fields_is_tuple invalid_models_tests.test_models_llm.ReverseRelatedIdentityTests.test_identity_reflects_db_constraint_difference invalid_models_tests.test_models_llm.ReverseRelatedIdentityTests.test_none_vs_empty_through_fields_identity_not_equal invalid_models_tests.test_models_llm.ReverseRelatedIdentityTests.test_set_contains_both_none_and_empty
coverage json -o coverage.json
: '>>>>> End Test Output'
