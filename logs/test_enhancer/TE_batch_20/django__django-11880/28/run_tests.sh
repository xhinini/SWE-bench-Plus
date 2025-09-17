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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_deepcopy_modifying_mapping_does_not_affect_other_field_mapping forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_deepcopy_modifying_mapping_does_not_affect_other_form_field_mapping forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_deepcopy_shared_inner_mutable_reflected_change_field forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_deepcopy_shared_inner_mutable_reflected_change_form forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_deepcopy_shared_object_used_by_two_fields forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_field_deepcopy_preserves_subclass_and_uncopyable forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_field_deepcopy_with_uncopyable_value_charfield forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_field_deepcopy_with_uncopyable_value_integerfield forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_form_deepcopy_dynamic_field_in_init_with_uncopyable forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_form_deepcopy_with_uncopyable_field
coverage json -o coverage.json
: '>>>>> End Test Output'
