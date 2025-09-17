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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.FieldOrderingRegressionTests._attach_field_to_model model_fields.tests_llm.FieldOrderingRegressionTests._make_field model_fields.tests_llm.FieldOrderingRegressionTests.test_bisect_insertion_preserves_order_for_equal_counters model_fields.tests_llm.FieldOrderingRegressionTests.test_bound_field_greater_than_unbound_field_when_counters_equal model_fields.tests_llm.FieldOrderingRegressionTests.test_multiple_unbound_and_bound_sorting_stability model_fields.tests_llm.FieldOrderingRegressionTests.test_sorting_mixed_fields_preserves_unbound_first model_fields.tests_llm.FieldOrderingRegressionTests.test_sorting_mixed_many_entries model_fields.tests_llm.FieldOrderingRegressionTests.test_transitive_ordering_unbound_modelA_modelB model_fields.tests_llm.FieldOrderingRegressionTests.test_unbound_field_orders_before_bound_field_when_counters_equal
coverage json -o coverage.json
: '>>>>> End Test Output'
