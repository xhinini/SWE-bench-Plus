#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 xor_lookups.tests_llm.XorAdditionalTests._compile_where_sql xor_lookups.tests_llm.XorAdditionalTests.setUpTestData xor_lookups.tests_llm.XorAdditionalTests.test_compile_does_not_raise_type_error_for_three_operands xor_lookups.tests_llm.XorAdditionalTests.test_filter_five_operands_results_and_compile xor_lookups.tests_llm.XorAdditionalTests.test_filter_four_operands_results xor_lookups.tests_llm.XorAdditionalTests.test_filter_three_operands_results xor_lookups.tests_llm.XorAdditionalTests.test_negated_xor_three_operands xor_lookups.tests_llm.XorAdditionalTests.test_nested_xor_groups_compile_and_produce_correct_results xor_lookups.tests_llm.XorAdditionalTests.test_sql_contains_mod_for_three_operands xor_lookups.tests_llm.XorAdditionalTests.test_sql_does_not_contain_mod_for_two_operands xor_lookups.tests_llm.XorAdditionalTests.test_xor_with_empty_in_and_more_than_two_operands
coverage json -o coverage.json
: '>>>>> End Test Output'
