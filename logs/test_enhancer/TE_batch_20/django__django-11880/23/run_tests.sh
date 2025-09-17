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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 forms_tests.tests.test_forms_llm.CustomObject.__init__ forms_tests.tests.test_forms_llm.FieldDeepCopyRegressionTests.test_field_deepcopy_nested_dict_value_identity forms_tests.tests.test_forms_llm.FieldDeepCopyRegressionTests.test_field_deepcopy_preserves_nested_custom_object_identity forms_tests.tests.test_forms_llm.FieldDeepCopyRegressionTests.test_field_deepcopy_preserves_nested_list_identity forms_tests.tests.test_forms_llm.FieldDeepCopyRegressionTests.test_field_deepcopy_reflects_mutation_on_nested_custom_object forms_tests.tests.test_forms_llm.FieldDeepCopyRegressionTests.test_field_deepcopy_reflects_mutation_on_nested_list forms_tests.tests.test_forms_llm.FieldDeepCopyRegressionTests.test_form_deepcopy_field_error_messages_share_nested_object_identity forms_tests.tests.test_forms_llm.FieldDeepCopyRegressionTests.test_form_deepcopy_shared_error_message_mutation_reflected_in_copies forms_tests.tests.test_forms_llm.FieldDeepCopyRegressionTests.test_form_deepcopy_shared_error_message_object_preserved_between_fields forms_tests.tests.test_forms_llm.FieldDeepCopyRegressionTests.test_multiple_deepcopies_preserve_same_nested_object_identity
coverage json -o coverage.json
: '>>>>> End Test Output'
