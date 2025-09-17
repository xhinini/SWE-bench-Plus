#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_datastructures_llm.OrderedSetReverseMutationTests.test_reversed_raises_on_add_new_key utils_tests.test_datastructures_llm.OrderedSetReverseMutationTests.test_reversed_raises_on_multiple_adds utils_tests.test_datastructures_llm.OrderedSetReverseMutationTests.test_reversed_raises_on_remove_existing_key utils_tests.test_datastructures_llm.OrderedSetReverseMutationTests.test_reversed_raises_on_setitem_new_key_in_underlying_dict utils_tests.test_datastructures_llm.OrderedSetReverseMutationTests.test_reversed_raises_when_underlying_dict_cleared
coverage json -o coverage.json
: '>>>>> End Test Output'
