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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 forms_tests.tests.test_forms_llm.FormsTestCaseFieldErrorMessagesShallowCopy.test_deepcopy_preserves_custom_object_value_reference forms_tests.tests.test_forms_llm.FormsTestCaseFieldErrorMessagesShallowCopy.test_deepcopy_preserves_list_mutation_reflected_in_copy_for_form_field forms_tests.tests.test_forms_llm.FormsTestCaseFieldErrorMessagesShallowCopy.test_deepcopy_preserves_list_value_reference forms_tests.tests.test_forms_llm.FormsTestCaseFieldErrorMessagesShallowCopy.test_deepcopy_preserves_mutable_in_error_messages_after_field_copy forms_tests.tests.test_forms_llm.FormsTestCaseFieldErrorMessagesShallowCopy.test_deepcopy_preserves_nested_dict_reference forms_tests.tests.test_forms_llm.FormsTestCaseFieldErrorMessagesShallowCopy.test_deepcopy_preserves_nested_list_identity forms_tests.tests.test_forms_llm.FormsTestCaseFieldErrorMessagesShallowCopy.test_deepcopy_preserves_shared_mutable_across_fields_in_form forms_tests.tests.test_forms_llm.FormsTestCaseFieldErrorMessagesShallowCopy.test_deepcopy_preserves_shared_value_identity_across_keys forms_tests.tests.test_forms_llm.FormsTestCaseFieldErrorMessagesShallowCopy.test_deepcopy_reflects_mutation_for_form_field forms_tests.tests.test_forms_llm.FormsTestCaseFieldErrorMessagesShallowCopy.test_deepcopy_shallow_for_multiple_deep_levels
coverage json -o coverage.json
: '>>>>> End Test Output'
