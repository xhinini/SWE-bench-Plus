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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 forms_tests.tests.test_forms_llm.DeepcopyErrorMessagesTests.test_deepcopy_does_not_deepcopy_error_message_value_types forms_tests.tests.test_forms_llm.DeepcopyErrorMessagesTests.test_deepcopy_many_forms_share_inner_value forms_tests.tests.test_forms_llm.DeepcopyErrorMessagesTests.test_deepcopy_preserves_reference_for_callable_value forms_tests.tests.test_forms_llm.DeepcopyErrorMessagesTests.test_dynamic_form_field_copy_shares_error_message_value forms_tests.tests.test_forms_llm.DeepcopyErrorMessagesTests.test_field_deepcopy_custom_object_shares_value_identity forms_tests.tests.test_forms_llm.DeepcopyErrorMessagesTests.test_field_deepcopy_list_value_shared forms_tests.tests.test_forms_llm.DeepcopyErrorMessagesTests.test_field_deepcopy_nested_dict_value_shared forms_tests.tests.test_forms_llm.DeepcopyErrorMessagesTests.test_form_field_deepcopy_preserves_inner_value_identity forms_tests.tests.test_forms_llm.DeepcopyErrorMessagesTests.test_multiple_field_copies_share_inner_value forms_tests.tests.test_forms_llm.DeepcopyErrorMessagesTests.test_subclass_field_deepcopy_shallow_error_message_values
coverage json -o coverage.json
: '>>>>> End Test Output'
