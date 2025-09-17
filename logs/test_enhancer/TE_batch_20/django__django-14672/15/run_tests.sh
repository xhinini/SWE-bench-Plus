#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.make_rel invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_equality_for_same_non_empty_through_fields invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_identity_through_fields_empty_list_is_hashable_tuple invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_identity_through_fields_empty_tuple_is_hashable_tuple
coverage json -o coverage.json
: '>>>>> End Test Output'
