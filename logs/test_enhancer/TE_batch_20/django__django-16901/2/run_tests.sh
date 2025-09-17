#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 xor_lookups.tests_llm.XorLookupsRegressionTests._expected_by_thresholds xor_lookups.tests_llm.XorLookupsRegressionTests.setUpTestData xor_lookups.tests_llm.XorLookupsRegressionTests.test_duplicate_conditions_in_xor xor_lookups.tests_llm.XorLookupsRegressionTests.test_empty_in_with_multiple_xor xor_lookups.tests_llm.XorLookupsRegressionTests.test_exclude_with_multiple_xor xor_lookups.tests_llm.XorLookupsRegressionTests.test_large_number_of_operands xor_lookups.tests_llm.XorLookupsRegressionTests.test_mixed_q_and_qs_xor xor_lookups.tests_llm.XorLookupsRegressionTests.test_negated_conditions_in_n_ary_xor xor_lookups.tests_llm.XorLookupsRegressionTests.test_pk_multiple_qs_xor xor_lookups.tests_llm.XorLookupsRegressionTests.test_qs_xor_four_querysets xor_lookups.tests_llm.XorLookupsRegressionTests.test_qs_xor_three_querysets xor_lookups.tests_llm.XorLookupsRegressionTests.test_values_list_multiple_xor
coverage json -o coverage.json
: '>>>>> End Test Output'
