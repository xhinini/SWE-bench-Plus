#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_forms_llm.UserCreationSaveM2MRegressionTests.test_password_is_set_correctly_when_save_m2m_hidden auth_tests.test_forms_llm.UserCreationSaveM2MRegressionTests.test_save_does_not_raise_if_save_m2m_is_hidden_on_instance auth_tests.test_forms_llm.UserCreationSaveM2MRegressionTests.test_saving_with_hidden_save_m2m_on_form_with_m2m_fields_does_not_raise
coverage json -o coverage.json
: '>>>>> End Test Output'
