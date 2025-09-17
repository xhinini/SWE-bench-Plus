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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 aggregation.tests_llm.test_sum_allows_distinct_in_aggregate_basic aggregation.tests_llm.test_sum_allows_distinct_in_annotate aggregation.tests_llm.test_sum_allows_distinct_with_decimal_field aggregation.tests_llm.test_sum_constructor_allows_distinct aggregation.tests_llm.test_sum_distinct_generates_distinct_in_sql aggregation.tests_llm.test_sum_distinct_in_values_annotate_grouping aggregation.tests_llm.test_sum_distinct_with_filter_expression aggregation.tests_llm.test_sum_get_repr_options_includes_distinct aggregation.tests_llm.test_sum_with_f_expression_and_distinct
coverage json -o coverage.json
: '>>>>> End Test Output'
