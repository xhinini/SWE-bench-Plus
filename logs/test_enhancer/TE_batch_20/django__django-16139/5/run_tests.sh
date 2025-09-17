#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 auth_tests.test_forms_llm.PasswordLinkTests.test_anchor_tag_present_in_help_text auth_tests.test_forms_llm.PasswordLinkTests.test_help_text_anchor_href_points_to_expected_relative_path auth_tests.test_forms_llm.PasswordLinkTests.test_help_text_includes_expected_relative_path_basic auth_tests.test_forms_llm.PasswordLinkTests.test_helptext_not_broken_when_password_field_removed auth_tests.test_forms_llm.PasswordLinkTests.test_joined_url_equals_password_change_url_standard_form auth_tests.test_forms_llm.PasswordLinkTests.test_joined_url_equals_password_change_url_via_to_field_admin_get_form auth_tests.test_forms_llm.PasswordLinkTests.test_link_contains_trailing_slash auth_tests.test_forms_llm.PasswordLinkTests.test_link_for_user_with_multi_digit_pk auth_tests.test_forms_llm.PasswordLinkTests.test_unicode_username_to_field_resolves_correctly
coverage json -o coverage.json
: '>>>>> End Test Output'
