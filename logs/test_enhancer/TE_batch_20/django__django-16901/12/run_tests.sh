#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 xor_lookups.tests_llm.XorWhereNodeTests.setUpTestData xor_lookups.tests_llm.XorWhereNodeTests.test_empty_in_three_operand_xor xor_lookups.tests_llm.XorWhereNodeTests.test_exclude_with_three_operand_xor xor_lookups.tests_llm.XorWhereNodeTests.test_five_operand_xor xor_lookups.tests_llm.XorWhereNodeTests.test_mixed_negation_xor xor_lookups.tests_llm.XorWhereNodeTests.test_pk_q_three_operand xor_lookups.tests_llm.XorWhereNodeTests.test_sql_compilation_three_operand_no_error xor_lookups.tests_llm.XorWhereNodeTests.test_stages_three_operand xor_lookups.tests_llm.XorWhereNodeTests.test_three_operand_xor xor_lookups.tests_llm.XorWhereNodeTests.test_two_operand_xor_works_without_mod xor_lookups.tests_llm.XorWhereNodeTests.test_values_list_three_operand
coverage json -o coverage.json
: '>>>>> End Test Output'
