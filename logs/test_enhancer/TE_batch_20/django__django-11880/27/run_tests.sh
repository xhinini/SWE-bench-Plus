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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_deepcopy_field_with_user_supplied_error_messages_dict forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_deepcopy_form_with_default_and_custom_error_messages forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_field_deepcopy_creates_new_error_messages_dict_but_keeps_nested_objects forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_form_deepcopy_preserves_nested_error_message_objects forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_modifying_nested_object_on_form_field_reflects_in_copied_form forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_mutating_nested_object_reflects_in_copy
coverage json -o coverage.json
: '>>>>> End Test Output'
