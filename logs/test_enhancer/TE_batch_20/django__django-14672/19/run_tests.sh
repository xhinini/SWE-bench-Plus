#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.make_rel invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.setUp invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_db_constraint_affects_identity invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_dict_keys_distinguish_none_and_empty_tuple invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_none_not_equal_empty_list invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_none_not_equal_empty_tuple invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_set_membership_distinguishes_none_and_empty_list
coverage json -o coverage.json
: '>>>>> End Test Output'
