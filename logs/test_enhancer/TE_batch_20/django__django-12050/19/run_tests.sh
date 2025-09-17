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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_query_llm.ResolveLookupValueNestedTests.test_build_filter_accepts_nested_iterable queries.test_query_llm.ResolveLookupValueNestedTests.test_deeply_nested_mixed_containers_resolves_all_Fs queries.test_query_llm.ResolveLookupValueNestedTests.test_deeply_nested_variant queries.test_query_llm.ResolveLookupValueNestedTests.test_list_of_list_with_F_resolves_inner_F queries.test_query_llm.ResolveLookupValueNestedTests.test_multiple_expressions_in_inner_list queries.test_query_llm.ResolveLookupValueNestedTests.test_nested_tuple_with_F queries.test_query_llm.ResolveLookupValueNestedTests.test_no_F_remaining_after_resolution queries.test_query_llm.ResolveLookupValueNestedTests.test_tuple_of_list_with_F_resolves_inner_F queries.test_query_llm._contains_instance
coverage json -o coverage.json
: '>>>>> End Test Output'
