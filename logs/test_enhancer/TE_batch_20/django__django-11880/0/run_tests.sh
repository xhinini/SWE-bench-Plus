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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 forms_tests.tests.test_forms_llm.CustomObject.__init__ forms_tests.tests.test_forms_llm.CustomObject.__repr__ forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_deepcopy_shallow_values_custom_object_identity forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_deepcopy_shallow_values_dict_identity forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_deepcopy_shallow_values_list_identity forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_field_subclass_default_error_messages_identity forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_form_deepcopy_error_messages_custom_reflection forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_multivaluefield_deepcopy_preserves_inner_field_error_messages_values forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_mutating_attribute_reflects_in_deepcopied_field forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_shallow_copy_behavior_with_nested_mutable_structure
coverage json -o coverage.json
: '>>>>> End Test Output'
