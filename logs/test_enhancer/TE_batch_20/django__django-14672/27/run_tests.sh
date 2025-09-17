#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_equality_with_same_list_contents invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_identity_contains_hashable_through_fields invalid_models_tests.test_models_llm.make_rel
coverage json -o coverage.json
: '>>>>> End Test Output'
