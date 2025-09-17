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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_query_llm.test_resolve_lookup_value_deeply_nested_tuples queries.test_query_llm.test_resolve_lookup_value_empty_iterables_preserved queries.test_query_llm.test_resolve_lookup_value_mixed_nesting queries.test_query_llm.test_resolve_lookup_value_multiple_levels_mixed_types queries.test_query_llm.test_resolve_lookup_value_nested_list_of_tuple queries.test_query_llm.test_resolve_lookup_value_nested_multiple_Fs queries.test_query_llm.test_resolve_lookup_value_nested_tuple_of_list queries.test_query_llm.test_resolve_lookup_value_nested_with_primitives_and_expressions queries.test_query_llm.test_resolve_lookup_value_preserves_list_type queries.test_query_llm.test_resolve_lookup_value_preserves_tuple_type
coverage json -o coverage.json
: '>>>>> End Test Output'
