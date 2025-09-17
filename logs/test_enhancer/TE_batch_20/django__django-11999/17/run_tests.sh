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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_existing_attribute_none_not_overwritten model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_existing_non_callable_attribute_not_overwritten model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_field_without_choices_does_not_create_display_method model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_iterator_choices_with_existing_method_not_overwritten model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_multiple_fields_one_user_defined_other_created model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_user_defined_classmethod_not_overwritten model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_user_defined_instance_method_not_overwritten model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_user_defined_staticmethod_not_overwritten
coverage json -o coverage.json
: '>>>>> End Test Output'
