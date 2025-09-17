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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_query_llm.TestQueryNestedIterables.test_deeply_nested_lists_resolve_F queries.test_query_llm.TestQueryNestedIterables.test_mixed_nested_iterables_resolve_all_Fs queries.test_query_llm.TestQueryNestedIterables.test_multiple_depth_mixed_iterables queries.test_query_llm.TestQueryNestedIterables.test_nested_empty_list_preserved queries.test_query_llm.TestQueryNestedIterables.test_nested_iterables_multiple_expressions queries.test_query_llm.TestQueryNestedIterables.test_nested_iterables_with_non_expression_elements queries.test_query_llm.TestQueryNestedIterables.test_nested_list_resolves_F queries.test_query_llm.TestQueryNestedIterables.test_nested_tuple_resolves_F
coverage json -o coverage.json
: '>>>>> End Test Output'
