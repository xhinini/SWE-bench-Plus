#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_datastructures_llm.OrderedSetReversedMutationTests.test_reversed_raises_on_add_new utils_tests.test_datastructures_llm.OrderedSetReversedMutationTests.test_reversed_raises_on_direct_dict_assignment utils_tests.test_datastructures_llm.OrderedSetReversedMutationTests.test_reversed_raises_on_discard_existing utils_tests.test_datastructures_llm.OrderedSetReversedMutationTests.test_reversed_raises_on_pop_from_underlying_dict utils_tests.test_datastructures_llm.OrderedSetReversedMutationTests.test_reversed_raises_on_remove
coverage json -o coverage.json
: '>>>>> End Test Output'
