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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_query_llm.ResolveLookupValueRecursiveTests.test_deeply_nested_mixture_resolves_all_Fs queries.test_query_llm.ResolveLookupValueRecursiveTests.test_list_of_tuples_resolves_inner_Fs queries.test_query_llm.ResolveLookupValueRecursiveTests.test_mixed_nested_structures_preserve_and_resolve queries.test_query_llm.ResolveLookupValueRecursiveTests.test_multiple_levels_of_nesting_all_resolved queries.test_query_llm.ResolveLookupValueRecursiveTests.test_nested_list_resolves_inner_F queries.test_query_llm.ResolveLookupValueRecursiveTests.test_nested_tuple_resolves_inner_F_and_preserves_tuple queries.test_query_llm.ResolveLookupValueRecursiveTests.test_tuple_containing_list_resolves_inner_and_preserves_types
coverage json -o coverage.json
: '>>>>> End Test Output'
