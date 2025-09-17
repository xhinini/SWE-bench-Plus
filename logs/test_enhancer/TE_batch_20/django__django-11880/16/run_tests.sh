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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_deepcopy_creates_independent_error_messages_dicts forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_deepcopy_field_shares_mutable_dict_value forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_deepcopy_field_shares_mutable_list_value forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_deepcopy_list_values_shared_across_copies_of_form forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_deepcopy_two_fields_sharing_same_value_keep_same_identity_in_copy forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_field_deepcopy_allows_mutation_to_propagate_to_copy forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_field_deepcopy_preserves_error_message_value_identity forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_form_deepcopy_preserves_field_error_messages_shallow forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_multiple_deepcopies_preserve_inner_value_identity forms_tests.tests.test_forms_llm.__repr__'] (forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.['Uncopyable.__init__', 'Uncopyable.__deepcopy__', 'Uncopyable)
coverage json -o coverage.json
: '>>>>> End Test Output'
