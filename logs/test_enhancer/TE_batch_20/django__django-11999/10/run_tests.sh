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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_field_with_no_choices_does_not_add_display model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_method_added_when_not_defined model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_multiple_fields_do_not_collide model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_preserve_classmethod_display model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_preserve_staticmethod_display model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_subclass_overrides_parent_method_and_is_preserved model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_user_defined_display_method_after_field model_fields.tests_llm.ContributeToClassDisplayMethodTests.test_user_defined_display_method_before_field
coverage json -o coverage.json
: '>>>>> End Test Output'
