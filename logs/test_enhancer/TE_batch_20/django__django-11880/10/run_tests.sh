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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 forms_tests.tests.test_forms_llm._make_custom_obj forms_tests.tests.test_forms_llm.test_choicefield_in_form_deepcopy_shares_nested_error_messages_value forms_tests.tests.test_forms_llm.test_field_deepcopy_shares_nested_error_messages_value_charfield forms_tests.tests.test_forms_llm.test_field_deepcopy_shares_nested_error_messages_value_choicefield forms_tests.tests.test_forms_llm.test_field_deepcopy_shares_nested_error_messages_value_integerfield forms_tests.tests.test_forms_llm.test_form_deepcopy_preserves_shared_object_between_fields forms_tests.tests.test_forms_llm.test_form_deepcopy_shares_field_error_messages_value forms_tests.tests.test_forms_llm.test_multifield_in_form_deepcopy_shares_nested_error_messages_value forms_tests.tests.test_forms_llm.test_multivaluefield_deepcopy_shares_nested_error_messages_value
coverage json -o coverage.json
: '>>>>> End Test Output'
