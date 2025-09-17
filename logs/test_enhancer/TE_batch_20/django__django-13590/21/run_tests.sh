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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 expressions.tests_llm.ResolveLookupValueIterableTests.setUpTestData expressions.tests_llm.ResolveLookupValueIterableTests.test_collections_namedtuple_used_with_in_lookup expressions.tests_llm.ResolveLookupValueIterableTests.test_collections_namedtuple_with_F_expressions_in_range expressions.tests_llm.ResolveLookupValueIterableTests.test_mixed_iterables_with_namedtuple_and_expressions expressions.tests_llm.ResolveLookupValueIterableTests.test_namedtuple_preserves_field_order_and_values_after_resolution expressions.tests_llm.ResolveLookupValueIterableTests.test_nested_namedtuple_inside_list_for_in_lookup expressions.tests_llm.ResolveLookupValueIterableTests.test_plain_list_of_F_expressions_in_range expressions.tests_llm.ResolveLookupValueIterableTests.test_plain_tuple_of_F_expressions_in_range expressions.tests_llm.ResolveLookupValueIterableTests.test_typing_namedtuple_used_with_in_lookup expressions.tests_llm.ResolveLookupValueIterableTests.test_typing_namedtuple_with_F_expressions_in_range
coverage json -o coverage.json
: '>>>>> End Test Output'
