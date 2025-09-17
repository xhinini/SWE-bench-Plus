#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_forms_llm.SaveM2MGuardTests._make_form_class auth_tests.test_forms_llm.SaveM2MGuardTests.setUp auth_tests.test_forms_llm.SaveM2MGuardTests.test_multiple_saves_with_hidden_save_m2m_do_not_raise auth_tests.test_forms_llm.SaveM2MGuardTests.test_password_set_correctly_when_save_m2m_hidden auth_tests.test_forms_llm.SaveM2MGuardTests.test_save_with_hidden_save_m2m_commit_true_does_not_raise auth_tests.test_forms_llm.SaveM2MGuardTests.test_save_with_property_raising_and_commit_false_does_not_raise auth_tests.test_forms_llm.SaveM2MGuardTests.test_save_with_save_m2m_property_raising_does_not_raise
coverage json -o coverage.json
: '>>>>> End Test Output'
