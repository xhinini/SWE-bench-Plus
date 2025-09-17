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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 project_template.test_settings_llm.TestReferrerPolicySettings._get_referrer_header project_template.test_settings_llm.TestReferrerPolicySettings.setUp project_template.test_settings_llm.TestReferrerPolicySettings.test_global_setting_is_same_origin project_template.test_settings_llm.TestReferrerPolicySettings.test_header_present_with_csrf_and_security_middleware project_template.test_settings_llm.TestReferrerPolicySettings.test_middleware_order_does_not_affect_header_emission project_template.test_settings_llm.TestReferrerPolicySettings.test_multiple_requests_have_consistent_header project_template.test_settings_llm.TestReferrerPolicySettings.test_no_header_when_security_middleware_absent project_template.test_settings_llm.TestReferrerPolicySettings.test_override_setting_to_custom_value_changes_header project_template.test_settings_llm.TestReferrerPolicySettings.test_override_setting_to_none_removes_header project_template.test_settings_llm.TestReferrerPolicySettings.test_response_header_present_with_project_template_middleware project_template.test_settings_llm.TestReferrerPolicySettings.test_response_header_present_with_security_middleware_alone project_template.test_settings_llm.TestReferrerPolicySettings.test_setting_change_and_reset_restores_default_header
coverage json -o coverage.json
: '>>>>> End Test Output'
