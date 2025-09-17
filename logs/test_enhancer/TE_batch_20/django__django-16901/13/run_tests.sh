#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 xor_lookups.tests_llm.AdditionalXorTests.setUpTestData xor_lookups.tests_llm.AdditionalXorTests.test_chained_queryset_xor_multiple xor_lookups.tests_llm.AdditionalXorTests.test_empty_in_with_multiple_xor xor_lookups.tests_llm.AdditionalXorTests.test_exclude_three_way_xor xor_lookups.tests_llm.AdditionalXorTests.test_five_way_xor_values_list xor_lookups.tests_llm.AdditionalXorTests.test_four_way_xor xor_lookups.tests_llm.AdditionalXorTests.test_pk_q_multiple xor_lookups.tests_llm.AdditionalXorTests.test_sql_compiles_no_error_for_many_children xor_lookups.tests_llm.AdditionalXorTests.test_three_way_xor xor_lookups.tests_llm.AdditionalXorTests.test_xor_with_negations_mix xor_lookups.tests_llm.bool_xor
coverage json -o coverage.json
: '>>>>> End Test Output'
