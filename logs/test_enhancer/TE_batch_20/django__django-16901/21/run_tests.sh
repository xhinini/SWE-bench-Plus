#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 xor_lookups.tests_llm.XorLookupsRegressionTests._expected_by_preds xor_lookups.tests_llm.XorLookupsRegressionTests.setUpTestData xor_lookups.tests_llm.XorLookupsRegressionTests.test_all_operands_false_stages xor_lookups.tests_llm.XorLookupsRegressionTests.test_empty_in_both xor_lookups.tests_llm.XorLookupsRegressionTests.test_empty_in_left xor_lookups.tests_llm.XorLookupsRegressionTests.test_five_q_objects_values_list xor_lookups.tests_llm.XorLookupsRegressionTests.test_negated_mixed_q_objects xor_lookups.tests_llm.XorLookupsRegressionTests.test_pk_q_two_operands xor_lookups.tests_llm.XorLookupsRegressionTests.test_querysets_chain_three xor_lookups.tests_llm.XorLookupsRegressionTests.test_querysets_xor_operator xor_lookups.tests_llm.XorLookupsRegressionTests.test_three_q_objects xor_lookups.tests_llm.XorLookupsRegressionTests.test_two_q_objects
coverage json -o coverage.json
: '>>>>> End Test Output'
