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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 forms_tests.tests.test_forms_llm.CustomMutable.__init__ forms_tests.tests.test_forms_llm.CustomMutable.__repr__ forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_deepcopy_makes_new_mapping_but_keeps_value_identity_custom_object forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_deepcopy_twice_shares_values_between_copies forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_errorlist_value_is_shared forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_form_deepcopy_preserves_error_message_value_identity forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_list_value_is_shared_between_original_and_copy forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_modifying_mutable_value_reflects_in_copy forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_multiple_copies_share_value_identity_but_not_mapping_object forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_nested_dict_value_is_shared_between_original_and_copy forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_nested_mutable_inside_list_is_shared_between_copies forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_reassigning_key_on_original_does_not_modify_copy_mapping
coverage json -o coverage.json
: '>>>>> End Test Output'
