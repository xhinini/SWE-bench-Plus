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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 expressions.tests_llm.ResolveLookupValueIterableTests.setUpTestData expressions.tests_llm.ResolveLookupValueIterableTests.test_collections_namedtuple_with_F_expressions expressions.tests_llm.ResolveLookupValueIterableTests.test_list_of_expressions_in_lookup expressions.tests_llm.ResolveLookupValueIterableTests.test_list_vs_tuple_behaviour expressions.tests_llm.ResolveLookupValueIterableTests.test_namedtuple_with_lazy_object_member expressions.tests_llm.ResolveLookupValueIterableTests.test_tuple_of_expressions_range expressions.tests_llm.ResolveLookupValueIterableTests.test_typing_namedtuple_with_F_expressions
coverage json -o coverage.json
: '>>>>> End Test Output'
