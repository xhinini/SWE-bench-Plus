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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 forms_tests.tests.test_forms_llm.FieldErrorMessagesDeepcopyTests.test_changing_attribute_on_error_message_object_reflects_in_copy forms_tests.tests.test_forms_llm.FieldErrorMessagesDeepcopyTests.test_deepcopy_with_value_that_refuses_deepcopy_does_not_raise forms_tests.tests.test_forms_llm.FieldErrorMessagesDeepcopyTests.test_form_field_deepcopy_shares_error_message_values forms_tests.tests.test_forms_llm.FieldErrorMessagesDeepcopyTests.test_list_of_custom_objects_elements_same_identity forms_tests.tests.test_forms_llm.FieldErrorMessagesDeepcopyTests.test_mutating_nested_dict_inner_list_reflects_in_copy forms_tests.tests.test_forms_llm.FieldErrorMessagesDeepcopyTests.test_mutating_nested_list_reflects_in_copy forms_tests.tests.test_forms_llm.FieldErrorMessagesDeepcopyTests.test_shallow_copy_preserves_custom_object_identity forms_tests.tests.test_forms_llm.FieldErrorMessagesDeepcopyTests.test_shallow_copy_preserves_dict_identity forms_tests.tests.test_forms_llm.FieldErrorMessagesDeepcopyTests.test_shallow_copy_preserves_list_identity
coverage json -o coverage.json
: '>>>>> End Test Output'
