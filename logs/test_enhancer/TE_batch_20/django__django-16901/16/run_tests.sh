#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 xor_lookups.tests_llm.AdditionalXorLookupsTests._expected_by_preds xor_lookups.tests_llm.AdditionalXorLookupsTests.setUpTestData xor_lookups.tests_llm.AdditionalXorLookupsTests.test_chained_parens_three_way xor_lookups.tests_llm.AdditionalXorLookupsTests.test_four_way_xor xor_lookups.tests_llm.AdditionalXorLookupsTests.test_mixed_negations_and_three_way xor_lookups.tests_llm.AdditionalXorLookupsTests.test_negated_three_way_xor xor_lookups.tests_llm.AdditionalXorLookupsTests.test_three_way_values_list xor_lookups.tests_llm.AdditionalXorLookupsTests.test_three_way_xor_filter xor_lookups.tests_llm.AdditionalXorLookupsTests.test_three_way_xor_negated_middle xor_lookups.tests_llm.AdditionalXorLookupsTests.test_xor_empty_in_with_three xor_lookups.tests_llm.AdditionalXorLookupsTests.test_xor_exclude_three xor_lookups.tests_llm.AdditionalXorLookupsTests.test_xor_pk_three
coverage json -o coverage.json
: '>>>>> End Test Output'
