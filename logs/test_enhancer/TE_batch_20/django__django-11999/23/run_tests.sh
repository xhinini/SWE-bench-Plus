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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.FieldDisplayOverrideTests.test_classmethod_attname_not_overridden_by_descriptor model_fields.tests_llm.FieldDisplayOverrideTests.test_falsy_attribute_prevents_override model_fields.tests_llm.FieldDisplayOverrideTests.test_iterator_choices_generates_display_method_when_missing model_fields.tests_llm.FieldDisplayOverrideTests.test_method_created_when_absent model_fields.tests_llm.FieldDisplayOverrideTests.test_mixin_defined_method_not_overwritten model_fields.tests_llm.FieldDisplayOverrideTests.test_multiple_fields_have_independent_display_methods model_fields.tests_llm.FieldDisplayOverrideTests.test_staticmethod_on_parent_not_overwritten model_fields.tests_llm.FieldDisplayOverrideTests.test_user_defined_method_not_overwritten
coverage json -o coverage.json
: '>>>>> End Test Output'
