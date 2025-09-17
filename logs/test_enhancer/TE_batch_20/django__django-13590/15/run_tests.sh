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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 expressions.tests_llm.ResolveLookupValueIterableTests._assert_resolved_same_type_and_value expressions.tests_llm.ResolveLookupValueIterableTests.setUp expressions.tests_llm.ResolveLookupValueIterableTests.test_deeply_nested_mix expressions.tests_llm.ResolveLookupValueIterableTests.test_list_of_namedtuple_with_weirdtuple expressions.tests_llm.ResolveLookupValueIterableTests.test_multiple_weirdtuple_elements expressions.tests_llm.ResolveLookupValueIterableTests.test_tuple_of_namedtuple_with_weirdtuple expressions.tests_llm.ResolveLookupValueIterableTests.test_weirdtuple_direct expressions.tests_llm.ResolveLookupValueIterableTests.test_weirdtuple_in_list expressions.tests_llm.ResolveLookupValueIterableTests.test_weirdtuple_in_mixed_iterable expressions.tests_llm.ResolveLookupValueIterableTests.test_weirdtuple_in_nested_list expressions.tests_llm.ResolveLookupValueIterableTests.test_weirdtuple_in_tuple expressions.tests_llm.ResolveLookupValueIterableTests.test_weirdtuple_inside_collections_namedtuple expressions.tests_llm.WeirdTuple.__new__
coverage json -o coverage.json
: '>>>>> End Test Output'
