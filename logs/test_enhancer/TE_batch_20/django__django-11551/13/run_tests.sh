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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 modeladmin.test_checks_llm.AdditionalListDisplayRegressionTests.test_descriptor_that_raises_but_field_is_many_to_many_reports_e109 modeladmin.test_checks_llm.AdditionalListDisplayRegressionTests.test_list_display_accepts_callables modeladmin.test_checks_llm.AdditionalListDisplayRegressionTests.test_many_to_many_field_reports_e109 modeladmin.test_checks_llm.AdditionalListDisplayRegressionTests.test_missing_field_error_contains_correct_id_and_message modeladmin.test_checks_llm.AdditionalListDisplayRegressionTests.test_missing_field_reports_e108 modeladmin.test_checks_llm.AdditionalListDisplayRegressionTests.test_model_method_allowed_in_list_display modeladmin.test_checks_llm.AdditionalListDisplayRegressionTests.test_modeladmin_method_takes_precedence_over_model_field modeladmin.test_checks_llm.AdditionalListDisplayRegressionTests.test_property_on_model_allowed_in_list_display
coverage json -o coverage.json
: '>>>>> End Test Output'
