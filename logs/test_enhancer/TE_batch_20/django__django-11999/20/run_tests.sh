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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_multiple_fields_each_get_its_display_method model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_preserve_classmethod model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_preserve_existing_callable_that_is_not_method model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_preserve_existing_instance_method model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_preserve_falsy_class_attribute model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_preserve_inherited_method_from_base_model model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_preserve_property_attribute model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_preserve_staticmethod
coverage json -o coverage.json
: '>>>>> End Test Output'
