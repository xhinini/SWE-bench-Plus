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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.FieldOrderingRegressionTests.setUp model_fields.tests_llm.FieldOrderingRegressionTests.test_heapq_nsmallest_returns_no_model model_fields.tests_llm.FieldOrderingRegressionTests.test_list_sort_places_no_model_first model_fields.tests_llm.FieldOrderingRegressionTests.test_min_returns_no_model model_fields.tests_llm.FieldOrderingRegressionTests.test_no_model_lt_with_model_direct model_fields.tests_llm.FieldOrderingRegressionTests.test_sort_stability_with_mixed_no_model_and_model_fields model_fields.tests_llm.FieldOrderingRegressionTests.test_sorted_places_no_model_first model_fields.tests_llm.FieldOrderingRegressionTests.test_sorted_three_fields_first_is_no_model
coverage json -o coverage.json
: '>>>>> End Test Output'
