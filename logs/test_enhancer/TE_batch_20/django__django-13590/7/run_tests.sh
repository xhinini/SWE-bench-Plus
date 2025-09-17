#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
export LANG=en_US.UTF-8
export LANGUAGE=en_US:en
export LC_ALL=en_US.UTF-8
export PYTHONIOENCODING=utf8
python --version && python -m pip install -U pip
python -m pip install -U 'coverage==6.2'

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 expressions.tests_llm.ResolveLookupValueIterableTests.setUp expressions.tests_llm.ResolveLookupValueIterableTests.test_custom_tuple_like_single_element expressions.tests_llm.ResolveLookupValueIterableTests.test_custom_tuple_like_with_expression_values expressions.tests_llm.ResolveLookupValueIterableTests.test_custom_tuple_like_with_fields_attribute_constructs_from_single_iterable expressions.tests_llm.ResolveLookupValueIterableTests.test_custom_tuple_like_with_large_number_of_elements expressions.tests_llm.ResolveLookupValueIterableTests.test_custom_tuple_like_with_nested_values expressions.tests_llm.ResolveLookupValueIterableTests.test_custom_tuple_like_with_three_elements
coverage json -o coverage.json
: '>>>>> End Test Output'
