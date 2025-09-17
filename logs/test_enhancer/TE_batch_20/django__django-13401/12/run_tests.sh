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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.FieldOrderHashEqTests.test_complex_sort_mixed_fields_respects_expected_order model_fields.tests_llm.FieldOrderHashEqTests.test_models_sorted_by_app_label_and_model_name_when_counters_equal model_fields.tests_llm.FieldOrderHashEqTests.test_no_model_fields_sorted_before_model_fields_when_creation_counter_equal model_fields.tests_llm.FieldOrderHashEqTests.test_sort_stability_with_multiple_no_model_and_model_mix model_fields.tests_llm.make_dummy_model
coverage json -o coverage.json
: '>>>>> End Test Output'
