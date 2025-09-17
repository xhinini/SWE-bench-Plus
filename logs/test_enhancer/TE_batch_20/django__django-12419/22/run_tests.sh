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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 project_template.test_settings_llm.TestReferrerPolicySettings._get_headers project_template.test_settings_llm.TestReferrerPolicySettings.setUp project_template.test_settings_llm.TestReferrerPolicySettings.test_default_referrer_policy_header_present project_template.test_settings_llm.TestReferrerPolicySettings.test_no_security_middleware_no_referrer_header project_template.test_settings_llm.TestReferrerPolicySettings.test_referrer_policy_custom_value_reflected project_template.test_settings_llm.TestReferrerPolicySettings.test_referrer_policy_empty_string_sets_empty_header project_template.test_settings_llm.TestReferrerPolicySettings.test_referrer_policy_header_exact_bytes_in_response project_template.test_settings_llm.TestReferrerPolicySettings.test_referrer_policy_non_string_is_cast_to_string project_template.test_settings_llm.TestReferrerPolicySettings.test_referrer_policy_none_omits_header project_template.test_settings_llm.TestReferrerPolicySettings.test_referrer_policy_persists_across_requests project_template.test_settings_llm.TestReferrerPolicySettings.test_referrer_policy_with_altered_middleware_order project_template.test_settings_llm.TestReferrerPolicySettings.test_referrer_policy_with_ssl_redirect_true
coverage json -o coverage.json
: '>>>>> End Test Output'
