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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 forms_tests.tests.test_forms_llm.ErrorMessagesDeepCopyRegressionTests.test_field_error_messages_identity_of_inner_object forms_tests.tests.test_forms_llm.ErrorMessagesDeepCopyRegressionTests.test_field_error_messages_mutation_via_copy_reflects_original forms_tests.tests.test_forms_llm.ErrorMessagesDeepCopyRegressionTests.test_field_error_messages_shallow_copy_reflects_mutation_from_original forms_tests.tests.test_forms_llm.ErrorMessagesDeepCopyRegressionTests.test_field_error_messages_with_list_mutation_via_copy_reflects_original forms_tests.tests.test_forms_llm.ErrorMessagesDeepCopyRegressionTests.test_field_error_messages_with_list_shared_identity forms_tests.tests.test_forms_llm.ErrorMessagesDeepCopyRegressionTests.test_form_field_error_messages_identity_of_inner_object forms_tests.tests.test_forms_llm.ErrorMessagesDeepCopyRegressionTests.test_form_field_error_messages_mutation_via_copy_reflects_original forms_tests.tests.test_forms_llm.ErrorMessagesDeepCopyRegressionTests.test_form_field_error_messages_shallow_copy_reflects_mutation_from_original forms_tests.tests.test_forms_llm.ErrorMessagesDeepCopyRegressionTests.test_form_field_error_messages_with_list_shared_identity forms_tests.tests.test_forms_llm.__init__'] (forms_tests.tests.test_forms_llm.ErrorMessagesDeepCopyRegressionTests.['CustomCharFieldWithList) forms_tests.tests.test_forms_llm.__init__'] (forms_tests.tests.test_forms_llm.ErrorMessagesDeepCopyRegressionTests.['CustomCharFieldWithObject) forms_tests.tests.test_forms_llm.__str__'] (forms_tests.tests.test_forms_llm.ErrorMessagesDeepCopyRegressionTests.['CustomMessage.__init__', 'CustomMessage)
coverage json -o coverage.json
: '>>>>> End Test Output'
