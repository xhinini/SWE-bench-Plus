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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_query_llm.ResolveLookupValueTests.setUp queries.test_query_llm.ResolveLookupValueTests.test_deeply_nested_resolves queries.test_query_llm.ResolveLookupValueTests.test_mixed_nested_types_resolve_all_expressions queries.test_query_llm.ResolveLookupValueTests.test_multiple_expressions_in_inner_iterable_are_all_resolved queries.test_query_llm.ResolveLookupValueTests.test_nested_list_resolves_inner_expressions queries.test_query_llm.ResolveLookupValueTests.test_nested_tuple_resolves_inner_expressions_and_preserves_types queries.test_query_llm.ResolveLookupValueTests.test_preserve_and_resolve_mixed_sequence_types
coverage json -o coverage.json
: '>>>>> End Test Output'
