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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 aggregation.tests_llm.test_as_sql_contains_distinct_for_avg aggregation.tests_llm.test_as_sql_contains_distinct_for_sum aggregation.tests_llm.test_avg_allows_distinct_flag_on_aggregate aggregation.tests_llm.test_avg_allows_distinct_on_publisher_books_annotate aggregation.tests_llm.test_get_repr_options_includes_distinct aggregation.tests_llm.test_sum_allows_distinct_flag_on_aggregate aggregation.tests_llm.test_sum_allows_distinct_on_publisher_books_aggregate aggregation.tests_llm.test_sum_distinct_on_duration_field aggregation.tests_llm.test_sum_with_case_and_distinct
coverage json -o coverage.json
: '>>>>> End Test Output'
