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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 forms_tests.tests.test_forms_llm.FieldErrorMessagesShallowCopyTests.test_deepcopy_preserves_shared_mutable_nested_structures forms_tests.tests.test_forms_llm.FieldErrorMessagesShallowCopyTests.test_deepcopy_two_fields_sharing_same_mutable_object_reflection forms_tests.tests.test_forms_llm.FieldErrorMessagesShallowCopyTests.test_field_deepcopy_shallow_copy_preserves_nested_dict_mutation forms_tests.tests.test_forms_llm.FieldErrorMessagesShallowCopyTests.test_field_deepcopy_shared_custom_object_mutation_reflected forms_tests.tests.test_forms_llm.FieldErrorMessagesShallowCopyTests.test_field_deepcopy_shared_list_mutation_reflected forms_tests.tests.test_forms_llm.FieldErrorMessagesShallowCopyTests.test_field_with_class_default_error_messages_mutable_list_shared forms_tests.tests.test_forms_llm.FieldErrorMessagesShallowCopyTests.test_form_deepcopy_field_with_class_default_error_messages_mutable_list_shared forms_tests.tests.test_forms_llm.FieldErrorMessagesShallowCopyTests.test_form_deepcopy_shared_custom_object_mutation_reflected forms_tests.tests.test_forms_llm.FieldErrorMessagesShallowCopyTests.test_form_deepcopy_shared_list_mutation_reflected
coverage json -o coverage.json
: '>>>>> End Test Output'
