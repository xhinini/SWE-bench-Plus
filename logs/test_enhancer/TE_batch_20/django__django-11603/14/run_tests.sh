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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 aggregation.tests_llm.test_aggregate_default_alias_with_distinct_for_avg aggregation.tests_llm.test_avg_allows_distinct_aggregate aggregation.tests_llm.test_count_star_with_filter_raises_valueerror aggregation.tests_llm.test_custom_aggregate_disallowing_distinct_raises aggregation.tests_llm.test_get_source_expressions_includes_filter_at_end aggregation.tests_llm.test_get_source_fields_excludes_filter aggregation.tests_llm.test_publisher_sum_distinct_book_prices aggregation.tests_llm.test_repr_options_include_distinct_for_avg aggregation.tests_llm.test_repr_options_include_distinct_for_sum aggregation.tests_llm.test_sum_allows_distinct_aggregate
coverage json -o coverage.json
: '>>>>> End Test Output'
