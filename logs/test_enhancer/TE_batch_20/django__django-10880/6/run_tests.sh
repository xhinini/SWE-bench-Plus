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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 aggregation.tests_llm.test_count_distinct_annotate_order_by aggregation.tests_llm.test_count_distinct_author_books aggregation.tests_llm.test_count_distinct_in_join_annotation aggregation.tests_llm.test_count_distinct_sql_aggregate aggregation.tests_llm.test_count_distinct_sql_annotate_query_str aggregation.tests_llm.test_count_distinct_sql_case_expression aggregation.tests_llm.test_count_distinct_sql_values_aggregate aggregation.tests_llm.test_count_distinct_sql_values_annotate aggregation.tests_llm.test_count_distinct_star_sql aggregation.tests_llm.test_count_repr_options_includes_distinct
coverage json -o coverage.json
: '>>>>> End Test Output'
