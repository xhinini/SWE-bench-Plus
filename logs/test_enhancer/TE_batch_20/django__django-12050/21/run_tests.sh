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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_query_llm.TestQuery.test_build_filter_with_nested_iterable_expression queries.test_query_llm.TestQuery.test_resolve_lookup_value_deep_mixed_nesting queries.test_query_llm.TestQuery.test_resolve_lookup_value_multiple_expressions_in_nested queries.test_query_llm.TestQuery.test_resolve_lookup_value_nested_list_resolves_F_to_SimpleCol queries.test_query_llm.TestQuery.test_resolve_lookup_value_nested_tuple_resolves_F_to_SimpleCol
coverage json -o coverage.json
: '>>>>> End Test Output'
