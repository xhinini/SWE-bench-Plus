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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 aggregation.tests_llm.test_avg_distinct_has_space aggregation.tests_llm.test_count_distinct_has_space aggregation.tests_llm.test_distinct_does_not_introduce_double_space aggregation.tests_llm.test_distinct_in_annotation_has_space aggregation.tests_llm.test_distinct_with_case_expression_has_space aggregation.tests_llm.test_max_distinct_has_space aggregation.tests_llm.test_multiple_distinct_aggregates_each_have_space aggregation.tests_llm.test_sum_distinct_has_space aggregation.tests_llm.test_values_list_annotation_distinct_has_space aggregation.tests_llm.test_values_with_distinct_aggregate_has_space
coverage json -o coverage.json
: '>>>>> End Test Output'
