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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_existing_descriptor_not_overwritten model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_existing_instance_method_not_overwritten model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_existing_method_when_field_name_provided_explicitly model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_existing_none_attribute_not_overwritten model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_existing_property_not_overwritten model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_existing_staticmethod_not_overwritten
coverage json -o coverage.json
: '>>>>> End Test Output'
