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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.test_query_llm.ResolveLookupValueTests.test_deeply_nested_three_levels queries.test_query_llm.ResolveLookupValueTests.test_inner_container_types_preserved queries.test_query_llm.ResolveLookupValueTests.test_mixed_list_and_tuple_nested queries.test_query_llm.ResolveLookupValueTests.test_multiple_nested_expressions queries.test_query_llm.ResolveLookupValueTests.test_nested_list_single_F queries.test_query_llm.ResolveLookupValueTests.test_nested_tuple_single_F queries.test_query_llm.ResolveLookupValueTests.test_nested_with_mixed_depths queries.test_query_llm.ResolveLookupValueTests.test_non_expression_scalars_and_nested queries.test_query_llm.ResolveLookupValueTests.test_outer_tuple_preserved_with_inner_list
coverage json -o coverage.json
: '>>>>> End Test Output'
