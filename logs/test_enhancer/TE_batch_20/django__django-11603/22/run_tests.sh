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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 aggregation.tests_llm.test_regression_avg_allows_distinct_in_aggregate aggregation.tests_llm.test_regression_avg_allows_distinct_in_annotate aggregation.tests_llm.test_regression_avg_construction_does_not_raise aggregation.tests_llm.test_regression_avg_used_in_expression aggregation.tests_llm.test_regression_default_alias_with_distinct aggregation.tests_llm.test_regression_sum_allows_distinct_in_aggregate aggregation.tests_llm.test_regression_sum_allows_distinct_in_annotate_reverse_fk aggregation.tests_llm.test_regression_sum_construction_does_not_raise aggregation.tests_llm.test_regression_sum_distinct_duration_field aggregation.tests_llm.test_regression_sum_used_in_expression
coverage json -o coverage.json
: '>>>>> End Test Output'
