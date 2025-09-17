#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 xor_lookups.tests_llm.XorLookupsRegressionTests._evaluate_preds xor_lookups.tests_llm.XorLookupsRegressionTests.setUpTestData xor_lookups.tests_llm.XorLookupsRegressionTests.test_empty_in_among_multiple xor_lookups.tests_llm.XorLookupsRegressionTests.test_exclude_with_xor xor_lookups.tests_llm.XorLookupsRegressionTests.test_five_operands_xor_values_list xor_lookups.tests_llm.XorLookupsRegressionTests.test_negated_mix_xor xor_lookups.tests_llm.XorLookupsRegressionTests.test_negated_whole_xor xor_lookups.tests_llm.XorLookupsRegressionTests.test_pk_two_operands xor_lookups.tests_llm.XorLookupsRegressionTests.test_querysets_xor_operator_multiple xor_lookups.tests_llm.XorLookupsRegressionTests.test_three_operands_xor_qs xor_lookups.tests_llm.XorLookupsRegressionTests.test_two_operands_xor_qs xor_lookups.tests_llm.XorLookupsRegressionTests.test_xor_with_mixed_q_and_queryset
coverage json -o coverage.json
: '>>>>> End Test Output'
