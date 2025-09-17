#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 invalid_models_tests.test_models_llm.TestManyToManyRelIdentity.setUp invalid_models_tests.test_models_llm.TestManyToManyRelIdentity.test_empty_list_and_empty_tuple_equal_to_each_other invalid_models_tests.test_models_llm.TestManyToManyRelIdentity.test_list_vs_tuple_with_same_content_equal
coverage json -o coverage.json
: '>>>>> End Test Output'
