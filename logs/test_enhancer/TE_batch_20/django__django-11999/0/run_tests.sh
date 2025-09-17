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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.DisplayOverrideRegressionTests.test_existing_attribute_none_is_preserved model_fields.tests_llm.DisplayOverrideRegressionTests.test_existing_descriptor_preserved model_fields.tests_llm.DisplayOverrideRegressionTests.test_method_added_when_absent model_fields.tests_llm.DisplayOverrideRegressionTests.test_mixin_provided_method_not_overridden model_fields.tests_llm.DisplayOverrideRegressionTests.test_no_display_method_created_when_choices_none model_fields.tests_llm.DisplayOverrideRegressionTests.test_property_not_overridden model_fields.tests_llm.DisplayOverrideRegressionTests.test_staticmethod_not_overridden model_fields.tests_llm.DisplayOverrideRegressionTests.test_user_defined_method_not_overridden
coverage json -o coverage.json
: '>>>>> End Test Output'
