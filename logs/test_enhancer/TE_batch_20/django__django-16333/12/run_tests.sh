#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_forms_llm.HiddenSaveM2MTests.test_hidden_save_m2m_basic_create_user auth_tests.test_forms_llm.HiddenSaveM2MTests.test_hidden_save_m2m_multiple_saves auth_tests.test_forms_llm.HiddenSaveM2MTests.test_hidden_save_m2m_normalizes_username auth_tests.test_forms_llm.HiddenSaveM2MTests.test_hidden_save_m2m_preserves_password_whitespace auth_tests.test_forms_llm.HiddenSaveM2MTests.test_hidden_save_m2m_sets_password auth_tests.test_forms_llm.HiddenSaveM2MTests.test_hidden_save_m2m_unicode_username auth_tests.test_forms_llm.HiddenSaveM2MTests.test_hidden_save_m2m_with_custom_user_model auth_tests.test_forms_llm.HiddenSaveM2MTests.test_hidden_save_m2m_with_extension_user_model auth_tests.test_forms_llm.HiddenSaveM2MTests.test_hidden_save_m2m_with_i18n_context auth_tests.test_forms_llm.HiddenSaveM2MTests.test_hidden_save_m2m_with_m2m_field_present_does_not_error
coverage json -o coverage.json
: '>>>>> End Test Output'
