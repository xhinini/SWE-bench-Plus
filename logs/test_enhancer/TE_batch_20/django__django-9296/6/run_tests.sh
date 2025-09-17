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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 pagination.tests_llm.PaginatorIterationRegressionTests.test_empty_list_allow_empty_first_page_false_yields_no_pages pagination.tests_llm.PaginatorIterationRegressionTests.test_empty_list_allow_empty_first_page_true_yields_one_empty_page pagination.tests_llm.PaginatorIterationRegressionTests.test_for_loop_iteration_collects_expected_page_object_lists pagination.tests_llm.PaginatorIterationRegressionTests.test_iter_returns_page_instances_and_matches_page_range pagination.tests_llm.PaginatorIterationRegressionTests.test_iteration_preserves_page_order_against_page_range pagination.tests_llm.PaginatorIterationRegressionTests.test_iteration_with_count_method_container pagination.tests_llm.PaginatorIterationRegressionTests.test_iterator_exhaustion_raises_stopiteration pagination.tests_llm.PaginatorIterationRegressionTests.test_iterator_independence_multiple_iter_calls pagination.tests_llm.PaginatorIterationRegressionTests.test_list_conversion_of_paginator pagination.tests_llm.PaginatorIterationRegressionTests.test_pages_from_iteration_support_sequence_protocol
coverage json -o coverage.json
: '>>>>> End Test Output'
