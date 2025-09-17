#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_forms_llm.PasswordLinkTests.setUp auth_tests.test_forms_llm.PasswordLinkTests.test_admin_get_form_with_to_field_uses_pk_in_helptext auth_tests.test_forms_llm.PasswordLinkTests.test_bound_and_unbound_forms_have_same_helptext auth_tests.test_forms_llm.PasswordLinkTests.test_encoded_username_does_not_affect_join_result auth_tests.test_forms_llm.PasswordLinkTests.test_helptext_contains_anchor_tag auth_tests.test_forms_llm.PasswordLinkTests.test_helptext_contains_two_level_relative_path auth_tests.test_forms_llm.PasswordLinkTests.test_helptext_uses_pk_not_username_when_to_field_set auth_tests.test_forms_llm.PasswordLinkTests.test_joined_url_matches_password_change_url auth_tests.test_forms_llm.PasswordLinkTests.test_large_pk_in_helptext auth_tests.test_forms_llm.PasswordLinkTests.test_no_exception_when_password_field_excluded
coverage json -o coverage.json
: '>>>>> End Test Output'
