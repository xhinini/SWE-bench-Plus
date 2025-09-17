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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.ContributeToClassDisplayTests.test_existing_staticmethod_preserved model_fields.tests_llm.ContributeToClassDisplayTests.test_metaclass_provided_attribute_preserved model_fields.tests_llm.ContributeToClassDisplayTests.test_multiple_fields_do_not_override_manual_method model_fields.tests_llm.ContributeToClassDisplayTests.test_no_choices_creates_no_method model_fields.tests_llm.ContributeToClassDisplayTests.test_non_callable_attribute_preserved model_fields.tests_llm.ContributeToClassDisplayTests.test_preexisting_method_before_field_not_overwritten model_fields.tests_llm.ContributeToClassDisplayTests.test_property_preserved
coverage json -o coverage.json
: '>>>>> End Test Output'
