#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_forms_llm.UserChangeFormPkLinkTests.setUpTestData auth_tests.test_forms_llm.UserChangeFormPkLinkTests.test_admin_to_field_access_still_resolves_to_pk_password_change auth_tests.test_forms_llm.UserChangeFormPkLinkTests.test_custom_model_subclass_userchangeform_includes_pk
coverage json -o coverage.json
: '>>>>> End Test Output'
