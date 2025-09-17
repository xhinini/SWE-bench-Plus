#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 xor_lookups.tests_llm.XorRegressionTests.setUpTestData xor_lookups.tests_llm.XorRegressionTests.test_xor_empty_in_combination xor_lookups.tests_llm.XorRegressionTests.test_xor_exclude_combination xor_lookups.tests_llm.XorRegressionTests.test_xor_five_queryset_operator xor_lookups.tests_llm.XorRegressionTests.test_xor_four_qs_values xor_lookups.tests_llm.XorRegressionTests.test_xor_many_operands_even_count_results_empty xor_lookups.tests_llm.XorRegressionTests.test_xor_mix_q_and_queryset xor_lookups.tests_llm.XorRegressionTests.test_xor_negated_operands xor_lookups.tests_llm.XorRegressionTests.test_xor_pk_multiple xor_lookups.tests_llm.XorRegressionTests.test_xor_three_qs_values xor_lookups.tests_llm.XorRegressionTests.test_xor_two_operands
coverage json -o coverage.json
: '>>>>> End Test Output'
