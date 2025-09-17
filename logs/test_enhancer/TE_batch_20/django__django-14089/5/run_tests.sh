#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_datastructures_llm.OrderedSetReversedMutationTests.test_reversed_add_while_iterating_raises utils_tests.test_datastructures_llm.OrderedSetReversedMutationTests.test_reversed_dict_clear_while_iterating_raises utils_tests.test_datastructures_llm.OrderedSetReversedMutationTests.test_reversed_dict_pop_while_iterating_raises utils_tests.test_datastructures_llm.OrderedSetReversedMutationTests.test_reversed_direct_dict_setitem_while_iterating_raises utils_tests.test_datastructures_llm.OrderedSetReversedMutationTests.test_reversed_remove_while_iterating_raises utils_tests.test_datastructures_llm.OrderedSetReversedMutationTests.test_reversed_update_via_dict_update_while_iterating_raises
coverage json -o coverage.json
: '>>>>> End Test Output'
