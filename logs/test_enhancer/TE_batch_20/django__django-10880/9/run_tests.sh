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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 aggregation.tests_llm.DistinctFormattingTests._last_sql_lower aggregation.tests_llm.DistinctFormattingTests.setUpTestData aggregation.tests_llm.DistinctFormattingTests.test_aggregate_multiple_distinct_counts_each_include_space aggregation.tests_llm.DistinctFormattingTests.test_count_distinct_has_space_in_aggregate_sql aggregation.tests_llm.DistinctFormattingTests.test_count_distinct_in_annotation_generates_space aggregation.tests_llm.DistinctFormattingTests.test_count_distinct_in_values_annotate_has_space aggregation.tests_llm.DistinctFormattingTests.test_count_non_distinct_does_not_contain_distinct_fragment aggregation.tests_llm.DistinctFormattingTests.test_count_star_sql_contains_count_star_with_space aggregation.tests_llm.DistinctFormattingTests.test_count_star_with_filter_raises aggregation.tests_llm.DistinctFormattingTests.test_distinct_false_with_annotation_does_not_introduce_distinct aggregation.tests_llm.DistinctFormattingTests.test_distinct_fragment_not_adjacent_to_expression_without_space aggregation.tests_llm.DistinctFormattingTests.test_values_then_aggregate_distinct_has_space
coverage json -o coverage.json
: '>>>>> End Test Output'
