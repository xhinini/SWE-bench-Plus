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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.assert_shallow_copied_message_value forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_field_deepcopy_preserves_error_message_identity_charfield forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_field_deepcopy_preserves_error_message_identity_choicefield forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_field_deepcopy_preserves_error_message_identity_field forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_field_deepcopy_preserves_error_message_identity_filefield forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_field_deepcopy_preserves_error_message_identity_imagefield forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_field_deepcopy_preserves_error_message_identity_integerfield forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_field_deepcopy_preserves_error_message_identity_multiplechoicefield forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_field_deepcopy_preserves_error_message_identity_regexfield forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_field_deepcopy_preserves_error_message_identity_urlfield forms_tests.tests.test_forms_llm.DeepCopyErrorMessagesTests.test_field_deepcopy_preserves_error_message_identity_uuidfield forms_tests.tests.test_forms_llm.MutableMessage.__init__ forms_tests.tests.test_forms_llm.MutableMessage.__repr__
coverage json -o coverage.json
: '>>>>> End Test Output'
