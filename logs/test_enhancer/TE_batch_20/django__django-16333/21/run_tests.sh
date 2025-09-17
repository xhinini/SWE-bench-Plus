#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_forms_llm.UserCreationFormM2MTests._make_form_class auth_tests.test_forms_llm.UserCreationFormM2MTests.setUp auth_tests.test_forms_llm.UserCreationFormM2MTests.test_custom_save_m2m_called_once auth_tests.test_forms_llm.UserCreationFormM2MTests.test_save_commit_false_then_save_m2m auth_tests.test_forms_llm.UserCreationFormM2MTests.test_save_multiple_times_idempotent auth_tests.test_forms_llm.UserCreationFormM2MTests.test_save_with_missing_save_m2m_attribute_does_not_raise auth_tests.test_forms_llm.UserCreationFormM2MTests.test_saves_empty_m2m_list auth_tests.test_forms_llm.UserCreationFormM2MTests.test_saves_m2m_on_commit_true_multiple_orgs auth_tests.test_forms_llm.UserCreationFormM2MTests.test_saves_m2m_on_commit_true_single_org auth_tests.test_forms_llm.UserCreationFormM2MTests.test_saves_m2m_with_initial_data auth_tests.test_forms_llm.UserCreationFormM2MTests.test_saves_m2m_with_integer_values
coverage json -o coverage.json
: '>>>>> End Test Output'
