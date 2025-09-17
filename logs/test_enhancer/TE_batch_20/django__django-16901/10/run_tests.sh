#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 xor_lookups.tests_llm.XorLookupsAdditionalTests._expected_by_predicates xor_lookups.tests_llm.XorLookupsAdditionalTests.setUpTestData xor_lookups.tests_llm.XorLookupsAdditionalTests.test_exclude_with_three_operands xor_lookups.tests_llm.XorLookupsAdditionalTests.test_four_operand_mixed_negation_and_q xor_lookups.tests_llm.XorLookupsAdditionalTests.test_many_operand_xor_values_list_consistency xor_lookups.tests_llm.XorLookupsAdditionalTests.test_multi_operand_with_empty_in xor_lookups.tests_llm.XorLookupsAdditionalTests.test_negated_terms_in_multi_xor xor_lookups.tests_llm.XorLookupsAdditionalTests.test_pk_q_three_operands xor_lookups.tests_llm.XorLookupsAdditionalTests.test_three_operand_q_objects xor_lookups.tests_llm.XorLookupsAdditionalTests.test_three_operand_queryset_xor_operator xor_lookups.tests_llm.XorLookupsAdditionalTests.test_values_list_with_multiple_xor_q
coverage json -o coverage.json
: '>>>>> End Test Output'
