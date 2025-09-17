#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.setUp invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_dict_keys_distinct_for_none_and_empty_list invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_hash_distinguishes_none_and_empty_list invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_hash_distinguishes_none_and_empty_tuple invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_identity_none_vs_empty_list_not_equal invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_identity_none_vs_empty_tuple_not_equal invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_identity_through_fields_element_values
coverage json -o coverage.json
: '>>>>> End Test Output'
