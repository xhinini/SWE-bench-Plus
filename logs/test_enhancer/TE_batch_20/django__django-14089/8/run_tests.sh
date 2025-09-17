#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_datastructures_llm.OrderedSetReversedMutationTests.test_reversed_multiple_iterators_raise_on_mutation utils_tests.test_datastructures_llm.OrderedSetReversedMutationTests.test_reversed_partial_consumption_then_mutate_raises utils_tests.test_datastructures_llm.OrderedSetReversedMutationTests.test_reversed_raises_on_add_during_iteration utils_tests.test_datastructures_llm.OrderedSetReversedMutationTests.test_reversed_raises_on_clear_during_iteration utils_tests.test_datastructures_llm.OrderedSetReversedMutationTests.test_reversed_raises_on_direct_dict_setitem_during_iteration utils_tests.test_datastructures_llm.OrderedSetReversedMutationTests.test_reversed_raises_on_remove_during_iteration
coverage json -o coverage.json
: '>>>>> End Test Output'
