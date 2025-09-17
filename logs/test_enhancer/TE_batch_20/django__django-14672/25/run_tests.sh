#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.create_rel invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_identity_element_for_empty_list_is_tuple invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_identity_element_for_empty_tuple_is_tuple invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_list_vs_tuple_with_same_values_are_equal
coverage json -o coverage.json
: '>>>>> End Test Output'
