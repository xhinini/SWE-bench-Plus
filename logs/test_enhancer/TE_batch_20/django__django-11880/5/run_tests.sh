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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 forms_tests.tests.test_forms_llm.CustomMessage.__init__ forms_tests.tests.test_forms_llm.CustomMessage.__repr__ forms_tests.tests.test_forms_llm.DeepcopyErrorMessagesTests.test_deepcopy_preserves_identity_for_dict_values forms_tests.tests.test_forms_llm.DeepcopyErrorMessagesTests.test_deepcopy_preserves_identity_for_mutable_values_in_form forms_tests.tests.test_forms_llm.DeepcopyErrorMessagesTests.test_field_and_copy_have_independent_dict_objects_but_shared_values forms_tests.tests.test_forms_llm.DeepcopyErrorMessagesTests.test_field_deepcopy_creates_new_dict_but_preserves_value_identity forms_tests.tests.test_forms_llm.DeepcopyErrorMessagesTests.test_field_deepcopy_mutating_nested_value_reflects_in_copy forms_tests.tests.test_forms_llm.DeepcopyErrorMessagesTests.test_field_deepcopy_with_list_value_preserves_identity forms_tests.tests.test_forms_llm.DeepcopyErrorMessagesTests.test_form_deepcopy_creates_new_field_error_messages_dict_but_preserves_value_identity forms_tests.tests.test_forms_llm.DeepcopyErrorMessagesTests.test_form_deepcopy_mutating_nested_value_reflects_in_copy forms_tests.tests.test_forms_llm.DeepcopyErrorMessagesTests.test_form_deepcopy_two_fields_sharing_same_custom_object_preserves_shared_reference
coverage json -o coverage.json
: '>>>>> End Test Output'
