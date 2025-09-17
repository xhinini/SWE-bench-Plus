#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_forms_llm.test_admin_get_form_to_field_joined_url_matches_password_change auth_tests.test_forms_llm.test_admin_get_form_to_field_uses_pk_in_helptext auth_tests.test_forms_llm.test_password_helptext_contains_expected_pk auth_tests.test_forms_llm.test_password_helptext_does_not_use_one_dot_relative auth_tests.test_forms_llm.test_password_helptext_href_contains_expected_path auth_tests.test_forms_llm.test_password_helptext_href_starts_with_double_dot_slash_double_dot auth_tests.test_forms_llm.test_password_link_for_inactive_user_uses_pk auth_tests.test_forms_llm.test_password_link_for_unusable_password_user_uses_pk auth_tests.test_forms_llm.test_password_link_for_user_with_plus_in_username_uses_pk
coverage json -o coverage.json
: '>>>>> End Test Output'
