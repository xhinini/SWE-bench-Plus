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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.GetFieldDisplayOverrideRegressionTests.test_does_not_override_property model_fields.tests_llm.GetFieldDisplayOverrideRegressionTests.test_does_not_override_staticmethod model_fields.tests_llm.GetFieldDisplayOverrideRegressionTests.test_field_name_param_does_not_override_unrelated_method model_fields.tests_llm.GetFieldDisplayOverrideRegressionTests.test_mixin_provided_method_not_overridden model_fields.tests_llm.GetFieldDisplayOverrideRegressionTests.test_no_get_display_added_when_choices_is_none model_fields.tests_llm.GetFieldDisplayOverrideRegressionTests.test_preserves_non_callable_attribute
coverage json -o coverage.json
: '>>>>> End Test Output'
