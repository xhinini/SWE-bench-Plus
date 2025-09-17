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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.ContributeToClassDisplayTests.test_classmethod_get_FIELD_display_not_overwritten model_fields.tests_llm.ContributeToClassDisplayTests.test_custom_display_method_not_overwritten model_fields.tests_llm.ContributeToClassDisplayTests.test_iterator_choices_create_display_method model_fields.tests_llm.ContributeToClassDisplayTests.test_no_get_FIELD_display_when_choices_is_none model_fields.tests_llm.ContributeToClassDisplayTests.test_non_callable_class_attribute_not_overwritten model_fields.tests_llm.ContributeToClassDisplayTests.test_property_getter_not_overwritten model_fields.tests_llm.ContributeToClassDisplayTests.test_staticmethod_get_FIELD_display_not_overwritten model_fields.tests_llm.ContributeToClassDisplayTests.test_subclass_override_preserved
coverage json -o coverage.json
: '>>>>> End Test Output'
