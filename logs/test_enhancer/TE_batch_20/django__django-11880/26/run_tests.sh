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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_custom_object_value_is_shared_between_shallow_copies forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_deepcopy_on_field_preserves_mutable_value_identity_for_lists forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_deepcopy_on_field_preserves_mutable_value_identity_for_nested_structures forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_form_field_error_messages_nested_list_shared forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_list_value_is_shared_between_shallow_copies forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_modifying_copy_affects_original_for_shared_nested_objects forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_multiple_fields_in_form_share_nested_values_after_deepcopy forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_multivaluefield_subfield_error_messages_share_nested_values forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_nested_dict_value_is_shared_between_shallow_copies
coverage json -o coverage.json
: '>>>>> End Test Output'
