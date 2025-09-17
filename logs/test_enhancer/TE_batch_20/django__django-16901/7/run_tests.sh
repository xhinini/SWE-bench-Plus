#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 xor_lookups.tests_llm.AdditionalXorTests._expected_nums xor_lookups.tests_llm.AdditionalXorTests._expected_values xor_lookups.tests_llm.AdditionalXorTests.setUpTestData xor_lookups.tests_llm.AdditionalXorTests.test_xor_empty_in_with_multiple xor_lookups.tests_llm.AdditionalXorTests.test_xor_exclude_three xor_lookups.tests_llm.AdditionalXorTests.test_xor_four_qs_filter xor_lookups.tests_llm.AdditionalXorTests.test_xor_negated_whole xor_lookups.tests_llm.AdditionalXorTests.test_xor_pk_mixed xor_lookups.tests_llm.AdditionalXorTests.test_xor_queryset_multiple xor_lookups.tests_llm.AdditionalXorTests.test_xor_stages_combination xor_lookups.tests_llm.AdditionalXorTests.test_xor_three_qs_filter xor_lookups.tests_llm.AdditionalXorTests.test_xor_values_list xor_lookups.tests_llm.AdditionalXorTests.test_xor_with_negations_three
coverage json -o coverage.json
: '>>>>> End Test Output'
