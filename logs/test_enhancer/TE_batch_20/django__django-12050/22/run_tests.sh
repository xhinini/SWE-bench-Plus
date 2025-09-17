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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_query_llm.test_deeply_nested_resolves_F queries.test_query_llm.test_list_of_tuple_resolves_F queries.test_query_llm.test_mixed_structure_resolves_F queries.test_query_llm.test_multiple_fields_inner_tuple queries.test_query_llm.test_multiple_inner_items_resolve_all queries.test_query_llm.test_nested_expression_other_than_F_resolves queries.test_query_llm.test_nested_list_resolves_F queries.test_query_llm.test_nested_tuple_pairs_resolve_F queries.test_query_llm.test_nested_tuple_resolves_F queries.test_query_llm.test_tuple_of_tuple_resolves_F
coverage json -o coverage.json
: '>>>>> End Test Output'
