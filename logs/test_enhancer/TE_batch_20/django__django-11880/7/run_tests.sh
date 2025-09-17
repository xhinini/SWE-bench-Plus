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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 forms_tests.tests.test_forms_llm.test_field_deepcopy_error_messages_value_identity_charfield forms_tests.tests.test_forms_llm.test_field_deepcopy_error_messages_value_identity_choicefield forms_tests.tests.test_forms_llm.test_field_deepcopy_error_messages_value_identity_datefield forms_tests.tests.test_forms_llm.test_field_deepcopy_error_messages_value_identity_field forms_tests.tests.test_forms_llm.test_field_deepcopy_error_messages_value_identity_imagefield forms_tests.tests.test_forms_llm.test_field_deepcopy_error_messages_value_identity_multiplechoicefield forms_tests.tests.test_forms_llm.test_field_deepcopy_error_messages_value_identity_multivaluefield forms_tests.tests.test_forms_llm.test_field_deepcopy_error_messages_value_identity_regexfield forms_tests.tests.test_forms_llm.test_field_deepcopy_error_messages_value_identity_typedchoicefield forms_tests.tests.test_forms_llm.test_field_deepcopy_error_messages_value_identity_uuidfield
coverage json -o coverage.json
: '>>>>> End Test Output'
