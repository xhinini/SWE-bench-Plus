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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 forms_tests.tests.test_forms_llm.CustomMessage.__init__ forms_tests.tests.test_forms_llm.CustomMessage.__repr__ forms_tests.tests.test_forms_llm.FieldDeepCopyTests.test_error_messages_shallow_copy_dicts_are_distinct_but_values_shared forms_tests.tests.test_forms_llm.FieldDeepCopyTests.test_field_deepcopy_shares_list_value_and_reflects_mutation forms_tests.tests.test_forms_llm.FieldDeepCopyTests.test_field_deepcopy_shares_mutable_error_message_object forms_tests.tests.test_forms_llm.FieldDeepCopyTests.test_field_deepcopy_shares_nested_dict_value_and_reflects_mutation forms_tests.tests.test_forms_llm.FieldDeepCopyTests.test_field_subclass_deepcopy_shares_mutable_error_message_object forms_tests.tests.test_forms_llm.FieldDeepCopyTests.test_form_deepcopy_shares_mutable_error_message_object forms_tests.tests.test_forms_llm.FieldDeepCopyTests.test_form_two_fields_share_same_mutable_message_object_after_deepcopy forms_tests.tests.test_forms_llm.FieldDeepCopyTests.test_list_value_shared_between_form_and_copy forms_tests.tests.test_forms_llm.FieldDeepCopyTests.test_multiple_copies_share_same_inner_object_as_original
coverage json -o coverage.json
: '>>>>> End Test Output'
