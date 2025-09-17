#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests._dummy_field invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_equality_and_hash_with_equivalent_lists invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_hashable_with_through_fields_list invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_identity_includes_db_constraint
coverage json -o coverage.json
: '>>>>> End Test Output'
