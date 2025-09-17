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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 project_template.test_settings_llm.TestReferrerPolicy.test_ajax_request_has_referrer_policy_header project_template.test_settings_llm.TestReferrerPolicy.test_default_referrer_policy_header_present project_template.test_settings_llm.TestReferrerPolicy.test_disable_referrer_policy_with_none project_template.test_settings_llm.TestReferrerPolicy.test_empty_string_policy_emits_empty_header_value project_template.test_settings_llm.TestReferrerPolicy.test_header_value_is_str_type project_template.test_settings_llm.TestReferrerPolicy.test_multiple_requests_produce_consistent_header project_template.test_settings_llm.TestReferrerPolicy.test_no_header_when_security_middleware_missing project_template.test_settings_llm.TestReferrerPolicy.test_override_referrer_policy_custom_value project_template.test_settings_llm.TestReferrerPolicy.test_unicode_policy_value_supported project_template.test_settings_llm.TestReferrerPolicy.test_whitespace_in_policy_is_preserved
coverage json -o coverage.json
: '>>>>> End Test Output'
