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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 aggregation.tests_llm.test_count_distinct_after_values_and_annotate aggregation.tests_llm.test_count_distinct_in_annotation_select aggregation.tests_llm.test_count_distinct_in_values_list_annotation aggregation.tests_llm.test_count_distinct_on_related_field aggregation.tests_llm.test_count_distinct_sql_case_expression aggregation.tests_llm.test_count_distinct_sql_on_annotated_field aggregation.tests_llm.test_count_distinct_sql_on_values aggregation.tests_llm.test_count_distinct_sql_simple aggregation.tests_llm.test_count_distinct_sql_with_f_expression aggregation.tests_llm.test_count_distinct_with_case_in_annotation
coverage json -o coverage.json
: '>>>>> End Test Output'
