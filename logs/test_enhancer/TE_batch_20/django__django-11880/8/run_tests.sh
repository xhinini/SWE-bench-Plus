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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 forms_tests.tests.test_forms_llm.test_deepcopy_error_messages_mapping_independent_at_top_level forms_tests.tests.test_forms_llm.test_deepcopy_error_messages_shallow_on_form_field forms_tests.tests.test_forms_llm.test_deepcopy_error_messages_shallow_with_custom_field_subclass forms_tests.tests.test_forms_llm.test_deepcopy_error_messages_shared_nested_for_multivaluefield forms_tests.tests.test_forms_llm.test_deepcopy_error_messages_shares_dict_nested_on_form_field forms_tests.tests.test_forms_llm.test_deepcopy_error_messages_shares_list_nested_on_form_field forms_tests.tests.test_forms_llm.test_deepcopy_error_messages_shares_nested_custom_object_on_field forms_tests.tests.test_forms_llm.test_deepcopy_error_messages_shares_nested_dict_value_on_field forms_tests.tests.test_forms_llm.test_deepcopy_error_messages_shares_nested_list_value_on_field forms_tests.tests.test_forms_llm.test_deepcopy_nested_mutation_via_copy_reflects_in_original
coverage json -o coverage.json
: '>>>>> End Test Output'
