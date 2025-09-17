#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 xor_lookups.tests_llm.XorLookupsExtraTests.setUpTestData xor_lookups.tests_llm.XorLookupsExtraTests.test_chained_queryset_xor_three_way xor_lookups.tests_llm.XorLookupsExtraTests.test_empty_in_with_multiple_xor_operands xor_lookups.tests_llm.XorLookupsExtraTests.test_five_way_xor_even_odd_behavior xor_lookups.tests_llm.XorLookupsExtraTests.test_four_way_xor xor_lookups.tests_llm.XorLookupsExtraTests.test_mixed_negated_and_nonnegated_many_operands xor_lookups.tests_llm.XorLookupsExtraTests.test_nested_xor_with_or_and_multiple_operands xor_lookups.tests_llm.XorLookupsExtraTests.test_pk_q_three_way xor_lookups.tests_llm.XorLookupsExtraTests.test_three_way_xor xor_lookups.tests_llm.XorLookupsExtraTests.test_values_list_flat_for_multiple_xor xor_lookups.tests_llm.XorLookupsExtraTests.test_xor_with_negations_and_multiple_operands
coverage json -o coverage.json
: '>>>>> End Test Output'
