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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_query_llm.TestResolveLookupValueNestedIterables.test_deeply_nested_iterable_resolves_inner_F queries.test_query_llm.TestResolveLookupValueNestedIterables.test_mixed_scalars_and_exprs_in_nested_iterable queries.test_query_llm.TestResolveLookupValueNestedIterables.test_nested_iterable_on_different_model_field queries.test_query_llm.TestResolveLookupValueNestedIterables.test_nested_iterables_multiple_exprs_resolve_all queries.test_query_llm.TestResolveLookupValueNestedIterables.test_nested_list_of_list_with_F_simple_col_true queries.test_query_llm.TestResolveLookupValueNestedIterables.test_nested_tuple_of_tuple_with_F queries.test_query_llm.TestResolveLookupValueNestedIterables.test_preserve_mixed_tuple_and_list_types
coverage json -o coverage.json
: '>>>>> End Test Output'
