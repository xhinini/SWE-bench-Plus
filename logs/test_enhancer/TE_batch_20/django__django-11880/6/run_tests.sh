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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 forms_tests.tests.test_forms_llm.test_field_deepcopy_error_messages_bytearray_identity forms_tests.tests.test_forms_llm.test_field_deepcopy_error_messages_custom_object_identity forms_tests.tests.test_forms_llm.test_field_deepcopy_error_messages_custom_object_mutation_reflects forms_tests.tests.test_forms_llm.test_field_deepcopy_error_messages_dict_identity forms_tests.tests.test_forms_llm.test_field_deepcopy_error_messages_dict_mutation_reflects forms_tests.tests.test_forms_llm.test_field_deepcopy_error_messages_list_identity forms_tests.tests.test_forms_llm.test_field_deepcopy_error_messages_list_mutation_reflects forms_tests.tests.test_forms_llm.test_field_deepcopy_error_messages_multiple_values_identity forms_tests.tests.test_forms_llm.test_field_deepcopy_error_messages_nested_mutable_identity forms_tests.tests.test_forms_llm.test_field_deepcopy_error_messages_set_identity
coverage json -o coverage.json
: '>>>>> End Test Output'
