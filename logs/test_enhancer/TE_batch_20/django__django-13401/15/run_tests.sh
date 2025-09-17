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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.FieldComparisonRegressionTests.make_field model_fields.tests_llm.FieldComparisonRegressionTests.make_stub_model model_fields.tests_llm.FieldComparisonRegressionTests.test_model_field_is_greater_than_no_model_field_when_counters_equal model_fields.tests_llm.FieldComparisonRegressionTests.test_model_ordering_uses_app_label_and_model_name_tuple model_fields.tests_llm.FieldComparisonRegressionTests.test_no_model_field_is_ordered_before_model_field_when_counters_equal model_fields.tests_llm.FieldComparisonRegressionTests.test_sorting_mixed_fields_puts_no_model_first_then_models_by_meta
coverage json -o coverage.json
: '>>>>> End Test Output'
