#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 xor_lookups.tests_llm.AdditionalXorTests._expected_by_conditions xor_lookups.tests_llm.AdditionalXorTests.setUpTestData xor_lookups.tests_llm.AdditionalXorTests.test_xor_count_matches_len xor_lookups.tests_llm.AdditionalXorTests.test_xor_exclude_multiple xor_lookups.tests_llm.AdditionalXorTests.test_xor_five_operands_values_list xor_lookups.tests_llm.AdditionalXorTests.test_xor_four_operands xor_lookups.tests_llm.AdditionalXorTests.test_xor_pk_multiple xor_lookups.tests_llm.AdditionalXorTests.test_xor_queryset_chain xor_lookups.tests_llm.AdditionalXorTests.test_xor_three_operands_simple xor_lookups.tests_llm.AdditionalXorTests.test_xor_two_operands_behavior xor_lookups.tests_llm.AdditionalXorTests.test_xor_with_empty_in_multiple xor_lookups.tests_llm.AdditionalXorTests.test_xor_with_negation_multiple
coverage json -o coverage.json
: '>>>>> End Test Output'
