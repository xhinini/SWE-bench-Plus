#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.setUp invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_db_constraint_difference_not_equal invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_dict_keys_both_present invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_empty_tuple_vs_none_not_equal invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_none_vs_empty_list_not_equal invalid_models_tests.test_models_llm.ManyToManyRelIdentityTests.test_set_contains_both_none_and_empty_list
coverage json -o coverage.json
: '>>>>> End Test Output'
