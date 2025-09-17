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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_deepcopy_error_messages_dicts_are_distinct_but_values_shared forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_deepcopy_preserves_shared_mutable_between_multiple_fields forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_field_deepcopy_mutating_nested_value_reflects_in_copy forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_field_deepcopy_shallow_error_messages_shared_value forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_form_deepcopy_mutating_nested_value_reflects_in_copy forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_form_deepcopy_shallow_error_messages_shared_value forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_multivaluefield_in_form_deepcopy_shallow_nested_values forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_multivaluefield_subfields_preserve_nested_error_message_identity forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_mutation_on_shared_nested_object_reflects_across_many_copies
coverage json -o coverage.json
: '>>>>> End Test Output'
