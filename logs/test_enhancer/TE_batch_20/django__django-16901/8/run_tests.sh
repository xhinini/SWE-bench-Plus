#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 xor_lookups.tests_llm.XorRegressionsTests.setUpTestData xor_lookups.tests_llm.XorRegressionsTests.test_empty_in_with_multiple_xor xor_lookups.tests_llm.XorRegressionsTests.test_exclude_with_multiple_xor xor_lookups.tests_llm.XorRegressionsTests.test_four_way_xor_filters xor_lookups.tests_llm.XorRegressionsTests.test_mixed_negated_and_nonnegated_operands xor_lookups.tests_llm.XorRegressionsTests.test_negated_entire_xor xor_lookups.tests_llm.XorRegressionsTests.test_nested_xor_parentheses xor_lookups.tests_llm.XorRegressionsTests.test_pk_multiple_xor xor_lookups.tests_llm.XorRegressionsTests.test_queryset_xor_chain xor_lookups.tests_llm.XorRegressionsTests.test_three_way_xor_filters xor_lookups.tests_llm.XorRegressionsTests.test_xor_with_negations_multiple
coverage json -o coverage.json
: '>>>>> End Test Output'
