#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.make_rel invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_identity_contains_make_hashable_for_empty_list invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_identity_contains_make_hashable_for_empty_tuple invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_two_rels_with_explicit_empty_list_are_equal
coverage json -o coverage.json
: '>>>>> End Test Output'
