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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 aggregation.tests_llm.test_regression_avg_allows_distinct_aggregate aggregation.tests_llm.test_regression_avg_allows_distinct_annotate aggregation.tests_llm.test_regression_avg_distinct_generates_distinct_in_sql aggregation.tests_llm.test_regression_avg_distinct_with_values_and_aggregate aggregation.tests_llm.test_regression_default_alias_with_distinct aggregation.tests_llm.test_regression_repr_includes_distinct_option aggregation.tests_llm.test_regression_sum_allows_distinct_annotate_numeric aggregation.tests_llm.test_regression_sum_allows_distinct_duration_aggregate aggregation.tests_llm.test_regression_sum_distinct_generates_distinct_in_sql aggregation.tests_llm.test_regression_sum_distinct_on_duration_annotate
coverage json -o coverage.json
: '>>>>> End Test Output'
