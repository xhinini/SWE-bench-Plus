#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 xor_lookups.tests_llm.XorRegressionTests.setUpTestData xor_lookups.tests_llm.XorRegressionTests.test_chained_querysets_xor xor_lookups.tests_llm.XorRegressionTests.test_empty_in_among_many xor_lookups.tests_llm.XorRegressionTests.test_exclude_with_multiple xor_lookups.tests_llm.XorRegressionTests.test_mixed_lookup_types xor_lookups.tests_llm.XorRegressionTests.test_nary_xor_matches_python_parity xor_lookups.tests_llm.XorRegressionTests.test_negated_clause_among_many xor_lookups.tests_llm.XorRegressionTests.test_three_querysets_overlap xor_lookups.tests_llm.XorRegressionTests.test_three_range_qs xor_lookups.tests_llm.XorRegressionTests.test_two_operand_xor_still_works xor_lookups.tests_llm.XorRegressionTests.test_values_list_for_nary_xor
coverage json -o coverage.json
: '>>>>> End Test Output'
