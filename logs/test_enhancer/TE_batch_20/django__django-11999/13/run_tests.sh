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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.GetFieldDisplayPreservationTests.test_existing_callable_attribute_of_various_kinds_preserved model_fields.tests_llm.GetFieldDisplayPreservationTests.test_existing_method_defined_after_field_is_preserved model_fields.tests_llm.GetFieldDisplayPreservationTests.test_existing_method_defined_before_field_is_preserved model_fields.tests_llm.GetFieldDisplayPreservationTests.test_field_with_custom_name_preserves_existing_method model_fields.tests_llm.GetFieldDisplayPreservationTests.test_multiple_fields_do_not_override_preexisting_method model_fields.tests_llm.GetFieldDisplayPreservationTests.test_no_get_FIELD_display_created_when_choices_is_none model_fields.tests_llm.GetFieldDisplayPreservationTests.test_property_get_FIELD_display_is_preserved model_fields.tests_llm.GetFieldDisplayPreservationTests.test_staticmethod_get_FIELD_display_is_preserved
coverage json -o coverage.json
: '>>>>> End Test Output'
