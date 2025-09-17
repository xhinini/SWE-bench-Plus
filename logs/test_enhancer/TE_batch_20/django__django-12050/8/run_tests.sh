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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_query_llm.TestResolveLookupValueNestedIterables.test_deeper_nesting_resolves_all_levels queries.test_query_llm.TestResolveLookupValueNestedIterables.test_list_containing_tuple_with_f queries.test_query_llm.TestResolveLookupValueNestedIterables.test_mixed_nested_structures queries.test_query_llm.TestResolveLookupValueNestedIterables.test_multiple_f_in_nested_list queries.test_query_llm.TestResolveLookupValueNestedIterables.test_nested_iterables_with_none_and_f queries.test_query_llm.TestResolveLookupValueNestedIterables.test_nested_list_resolves_inner_f queries.test_query_llm.TestResolveLookupValueNestedIterables.test_nested_tuple_resolves_inner_f_and_preserves_tuple queries.test_query_llm.TestResolveLookupValueNestedIterables.test_tuple_of_tuples_nested_f_resolution
coverage json -o coverage.json
: '>>>>> End Test Output'
