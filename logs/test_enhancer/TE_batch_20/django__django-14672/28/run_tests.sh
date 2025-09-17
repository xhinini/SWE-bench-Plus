#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_dict_keys_distinct_for_none_and_empty_list invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_equality_between_none_and_empty_list_false invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_equality_list_vs_tuple_same_contents invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_hash_difference_between_none_and_empty_list invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_identity_element_for_empty_list_is_tuple invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_identity_element_for_empty_tuple_is_tuple invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_identity_includes_hashable_through_fields_type
coverage json -o coverage.json
: '>>>>> End Test Output'
