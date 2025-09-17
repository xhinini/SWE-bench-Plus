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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.FieldOrderingRegressionTests._make_bound model_fields.tests_llm.FieldOrderingRegressionTests._make_unbound model_fields.tests_llm.FieldOrderingRegressionTests.test_bisect_insertion_places_unbound_before_bound model_fields.tests_llm.FieldOrderingRegressionTests.test_inplace_sort_swaps_bound_and_unbound_when_creation_counter_equal model_fields.tests_llm.FieldOrderingRegressionTests.test_mixed_initial_ordering_sorted_result_consistent model_fields.tests_llm.FieldOrderingRegressionTests.test_multiple_insertions_preserve_no_model_first_order model_fields.tests_llm.FieldOrderingRegressionTests.test_sort_with_multiple_mixed_places_all_unbound_before_models model_fields.tests_llm.FieldOrderingRegressionTests.test_sorted_swaps_bound_and_unbound_when_creation_counter_equal model_fields.tests_llm.FieldOrderingRegressionTests.test_unbound_field_is_less_than_bound_field_when_creation_counter_equal
coverage json -o coverage.json
: '>>>>> End Test Output'
