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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_query_llm.TestResolveLookupValueNestedIterables.test_resolve_deeply_nested_three_levels queries.test_query_llm.TestResolveLookupValueNestedIterables.test_resolve_list_of_tuples_with_F queries.test_query_llm.TestResolveLookupValueNestedIterables.test_resolve_list_with_nonexpr_and_nested_expr queries.test_query_llm.TestResolveLookupValueNestedIterables.test_resolve_mixed_list_tuple_nested_F queries.test_query_llm.TestResolveLookupValueNestedIterables.test_resolve_nested_list_single_F queries.test_query_llm.TestResolveLookupValueNestedIterables.test_resolve_nested_mixed_structures_preserve_types_and_resolve queries.test_query_llm.TestResolveLookupValueNestedIterables.test_resolve_nested_tuple_single_F queries.test_query_llm.TestResolveLookupValueNestedIterables.test_resolve_tuple_of_tuple_nested_F queries.test_query_llm.TestResolveLookupValueNestedIterables.test_resolve_tuple_with_list_containing_tuple_F
coverage json -o coverage.json
: '>>>>> End Test Output'
