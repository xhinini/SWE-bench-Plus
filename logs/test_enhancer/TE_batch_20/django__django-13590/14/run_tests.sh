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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 expressions.tests_llm.ResolveLookupValueIterableTests.setUp expressions.tests_llm.ResolveLookupValueIterableTests.setUpTestData expressions.tests_llm.ResolveLookupValueIterableTests.test_empty_list_and_empty_tuple expressions.tests_llm.ResolveLookupValueIterableTests.test_iterable_of_F_expressions_preserves_container expressions.tests_llm.ResolveLookupValueIterableTests.test_list_of_values_returns_list expressions.tests_llm.ResolveLookupValueIterableTests.test_list_subclass_preserves_type expressions.tests_llm.ResolveLookupValueIterableTests.test_namedtuple_from_typing_preserves_type expressions.tests_llm.ResolveLookupValueIterableTests.test_namedtuple_preserves_type_and_values expressions.tests_llm.ResolveLookupValueIterableTests.test_nested_namedtuple_and_lists expressions.tests_llm.ResolveLookupValueIterableTests.test_tuple_of_values_returns_tuple expressions.tests_llm.ResolveLookupValueIterableTests.test_tuple_subclass_preserves_type
coverage json -o coverage.json
: '>>>>> End Test Output'
