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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.FieldOrderingRegressionTests._make_field model_fields.tests_llm.FieldOrderingRegressionTests.test_bound_field_greater_than_unbound_field_when_counters_equal model_fields.tests_llm.FieldOrderingRegressionTests.test_min_max_with_mixed_bound_and_unbound_equal_counters model_fields.tests_llm.FieldOrderingRegressionTests.test_multiple_sorts_consistent_order_for_mixed_fields model_fields.tests_llm.FieldOrderingRegressionTests.test_sort_mixed_fields_with_equal_counters_puts_unbound_first model_fields.tests_llm.FieldOrderingRegressionTests.test_unbound_field_is_less_than_bound_field_when_counters_equal
coverage json -o coverage.json
: '>>>>> End Test Output'
