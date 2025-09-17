#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.make_rel invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_db_constraint_affects_identity invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_list_vs_tuple_equality invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_many_to_many_rel_in_set_uniqueness_non_empty
coverage json -o coverage.json
: '>>>>> End Test Output'
