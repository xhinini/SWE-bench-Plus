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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 forms_tests.tests.test_forms_llm.CustomObject.__init__ forms_tests.tests.test_forms_llm.CustomObject.__repr__ forms_tests.tests.test_forms_llm.RegressionDeepCopyErrorMessagesTests.test_deepcopy_preserves_custom_object_identity_on_field forms_tests.tests.test_forms_llm.RegressionDeepCopyErrorMessagesTests.test_deepcopy_preserves_custom_object_identity_on_multivalue_field forms_tests.tests.test_forms_llm.RegressionDeepCopyErrorMessagesTests.test_deepcopy_preserves_nested_value_identity forms_tests.tests.test_forms_llm.RegressionDeepCopyErrorMessagesTests.test_deepcopy_preserves_shared_error_message_object_across_fields_in_form
coverage json -o coverage.json
: '>>>>> End Test Output'
