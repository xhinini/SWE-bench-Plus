#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_equality_for_two_instances_with_empty_list invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_equality_for_two_instances_with_empty_tuple invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_identity_element_type_for_empty_list_is_tuple_and_hashable invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_identity_through_fields_empty_list_is_tuple invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_identity_through_fields_empty_tuple_is_tuple invalid_models_tests.test_models_llm._create_rel invalid_models_tests.test_models_llm._make_stub_field invalid_models_tests.test_models_llm._make_stub_model
coverage json -o coverage.json
: '>>>>> End Test Output'
