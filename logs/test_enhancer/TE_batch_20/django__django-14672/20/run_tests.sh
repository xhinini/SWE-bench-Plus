#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.make_rel invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_identity_contains_frozenset_for_empty_set invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_identity_contains_tuple_for_empty_list invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_identity_contains_tuple_for_empty_tuple
coverage json -o coverage.json
: '>>>>> End Test Output'
