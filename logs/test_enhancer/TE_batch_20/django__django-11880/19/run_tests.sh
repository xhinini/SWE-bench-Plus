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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 forms_tests.tests.test_forms_llm.FieldDeepCopyErrorMessagesTests.test_copying_multiple_fields_in_form_shares_mutable_values forms_tests.tests.test_forms_llm.FieldDeepCopyErrorMessagesTests.test_deepcopy_field_shares_mutable_object forms_tests.tests.test_forms_llm.FieldDeepCopyErrorMessagesTests.test_deepcopy_form_shares_mutable_object forms_tests.tests.test_forms_llm.FieldDeepCopyErrorMessagesTests.test_deepcopy_preserves_shared_inner_object_identity forms_tests.tests.test_forms_llm.FieldDeepCopyErrorMessagesTests.test_deepcopy_with_nested_mutable_in_error_messages forms_tests.tests.test_forms_llm.FieldDeepCopyErrorMessagesTests.test_form_deepcopy_modifying_inner_list_reflects forms_tests.tests.test_forms_llm.FieldDeepCopyErrorMessagesTests.test_mutable_dict_shared_between_copies forms_tests.tests.test_forms_llm.FieldDeepCopyErrorMessagesTests.test_mutable_list_shared_between_copies forms_tests.tests.test_forms_llm.MutableMessage.__init__ forms_tests.tests.test_forms_llm.MutableMessage.__str__
coverage json -o coverage.json
: '>>>>> End Test Output'
