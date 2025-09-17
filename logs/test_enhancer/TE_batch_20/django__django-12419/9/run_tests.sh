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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 project_template.test_settings_llm.TestReferrerPolicySettings._get_headers project_template.test_settings_llm.TestReferrerPolicySettings.setUp project_template.test_settings_llm.TestReferrerPolicySettings.test_custom_value_set_in_header project_template.test_settings_llm.TestReferrerPolicySettings.test_debug_true_header_present project_template.test_settings_llm.TestReferrerPolicySettings.test_default_referrer_policy_present project_template.test_settings_llm.TestReferrerPolicySettings.test_false_value_removes_header project_template.test_settings_llm.TestReferrerPolicySettings.test_header_absent_without_security_middleware project_template.test_settings_llm.TestReferrerPolicySettings.test_header_present_with_custom_middleware_order project_template.test_settings_llm.TestReferrerPolicySettings.test_multiple_requests_do_not_accumulate_headers project_template.test_settings_llm.TestReferrerPolicySettings.test_no_duplicate_header_when_setting_same_as_default project_template.test_settings_llm.TestReferrerPolicySettings.test_override_to_empty_string_removes_header project_template.test_settings_llm.TestReferrerPolicySettings.test_override_to_none_removes_header
coverage json -o coverage.json
: '>>>>> End Test Output'
