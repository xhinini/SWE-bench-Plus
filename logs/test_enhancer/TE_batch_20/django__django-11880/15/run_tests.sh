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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesRegressionTests.test_adding_key_to_copy_does_not_affect_original_mapping forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesRegressionTests.test_deepcopy_on_form_with_dynamic_field_creation_preserves_shared_values forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesRegressionTests.test_deepcopy_preserves_dict_value_identity_in_error_messages forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesRegressionTests.test_deepcopy_preserves_list_value_identity_in_error_messages forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesRegressionTests.test_field_deepcopy_shares_nested_object_identity_and_mutation forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesRegressionTests.test_form_deepcopy_shares_field_error_messages_values forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesRegressionTests.test_form_instance_deepcopy_mutation_reflected forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesRegressionTests.test_multivaluefield_deepcopy_shares_error_message_values forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesRegressionTests.test_shared_object_between_multiple_fields_preserved_across_deepcopy
coverage json -o coverage.json
: '>>>>> End Test Output'
