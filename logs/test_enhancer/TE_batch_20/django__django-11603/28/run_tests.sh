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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 aggregation.tests_llm.DistinctAggregateTests.test_aggregate_without_allow_distinct_raises aggregation.tests_llm.DistinctAggregateTests.test_get_source_fields_excludes_filter aggregation.tests_llm.DistinctAggregateTests.test_resolve_expression_raises_on_nested_aggregate aggregation.tests_llm.DistinctAggregateTests.test_set_source_expressions_pops_filter
coverage json -o coverage.json
: '>>>>> End Test Output'
