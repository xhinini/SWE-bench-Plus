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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_adds_display_method_when_absent model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_does_not_override_classmethod_attribute model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_does_not_override_existing_method_on_model model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_does_not_override_if_attribute_is_empty_string model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_does_not_override_if_attribute_is_none model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_does_not_override_if_attribute_is_zero model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_does_not_override_property_attribute
coverage json -o coverage.json
: '>>>>> End Test Output'
