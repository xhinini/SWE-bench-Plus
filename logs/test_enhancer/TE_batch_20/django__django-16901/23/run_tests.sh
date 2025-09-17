#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 xor_lookups.tests_llm.XorLookupsConversionTests._force_no_xor_support xor_lookups.tests_llm.XorLookupsConversionTests.setUpTestData xor_lookups.tests_llm.XorLookupsConversionTests.test_conversion_empty_in xor_lookups.tests_llm.XorLookupsConversionTests.test_conversion_exclude xor_lookups.tests_llm.XorLookupsConversionTests.test_conversion_five_operands xor_lookups.tests_llm.XorLookupsConversionTests.test_conversion_negated xor_lookups.tests_llm.XorLookupsConversionTests.test_conversion_negated_full xor_lookups.tests_llm.XorLookupsConversionTests.test_conversion_pk_q xor_lookups.tests_llm.XorLookupsConversionTests.test_conversion_stages xor_lookups.tests_llm.XorLookupsConversionTests.test_conversion_three_operands xor_lookups.tests_llm.XorLookupsConversionTests.test_conversion_two_operands xor_lookups.tests_llm.XorLookupsConversionTests.test_conversion_values_list_parity
coverage json -o coverage.json
: '>>>>> End Test Output'
