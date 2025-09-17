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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 forms_tests.tests.test_forms_llm.FieldDeepcopyErrorMessagesTests.test_deepcopy_field_with_uncopyable_value_shares_nested_value forms_tests.tests.test_forms_llm.FieldDeepcopyErrorMessagesTests.test_deepcopy_form_fields_error_messages_independence forms_tests.tests.test_forms_llm.FieldDeepcopyErrorMessagesTests.test_deepcopy_mixed_uncopyable_and_mutable_values forms_tests.tests.test_forms_llm.FieldDeepcopyErrorMessagesTests.test_deepcopy_nested_list_mutation_reflected_in_copy forms_tests.tests.test_forms_llm.FieldDeepcopyErrorMessagesTests.test_deepcopy_preserves_shared_mutable_dict_value forms_tests.tests.test_forms_llm.FieldDeepcopyErrorMessagesTests.test_deepcopy_preserves_shared_mutable_list_value forms_tests.tests.test_forms_llm.FieldDeepcopyErrorMessagesTests.test_deepcopy_replacing_nested_value_does_not_change_copy_nested forms_tests.tests.test_forms_llm.Uncopyable.__deepcopy__ forms_tests.tests.test_forms_llm.Uncopyable.__init__ forms_tests.tests.test_forms_llm.Uncopyable.__repr__
coverage json -o coverage.json
: '>>>>> End Test Output'
