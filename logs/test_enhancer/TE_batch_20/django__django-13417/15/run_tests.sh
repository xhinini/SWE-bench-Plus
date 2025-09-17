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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 queries.tests_llm.GroupByOrderedTests.test_annotate_sets_group_by_blocks_default_ordering queries.tests_llm.GroupByOrderedTests.test_annotate_then_explicit_order_by_preserved queries.tests_llm.GroupByOrderedTests.test_default_ordering_none_and_group_by queries.tests_llm.GroupByOrderedTests.test_direct_group_by_flag_blocks_default_ordering queries.tests_llm.GroupByOrderedTests.test_empty_queryset_stays_ordered_even_if_group_by_true queries.tests_llm.GroupByOrderedTests.test_extra_order_by_overrides_group_by queries.tests_llm.GroupByOrderedTests.test_manual_group_by_and_extra_flags queries.tests_llm.GroupByOrderedTests.test_multi_field_values_with_group_by queries.tests_llm.GroupByOrderedTests.test_values_annotate_group_by_blocks_default_ordering queries.tests_llm.GroupByOrderedTests.test_values_annotate_then_order_by_explicit
coverage json -o coverage.json
: '>>>>> End Test Output'
