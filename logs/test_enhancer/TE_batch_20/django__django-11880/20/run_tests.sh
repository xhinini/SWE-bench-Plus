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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 forms_tests.tests.test_forms_llm.FormsTestCase.test_custom_field_subclass_deepcopy_error_messages_shallow_inner forms_tests.tests.test_forms_llm.FormsTestCase.test_deepcopy_preserves_shared_inner_object_between_multiple_fields forms_tests.tests.test_forms_llm.FormsTestCase.test_field_deepcopy_shares_inner_mutable_error_message_list forms_tests.tests.test_forms_llm.FormsTestCase.test_field_deepcopy_shares_inner_mutable_error_message_nested_dict forms_tests.tests.test_forms_llm.FormsTestCase.test_field_deepcopy_shares_inner_mutable_error_message_object forms_tests.tests.test_forms_llm.FormsTestCase.test_form_deepcopy_shares_inner_mutable_error_message_list forms_tests.tests.test_forms_llm.FormsTestCase.test_form_deepcopy_shares_inner_mutable_error_message_nested_dict forms_tests.tests.test_forms_llm.FormsTestCase.test_form_deepcopy_shares_inner_mutable_error_message_object
coverage json -o coverage.json
: '>>>>> End Test Output'
