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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 project_template.test_settings_llm.TestReferrerPolicy.setUp project_template.test_settings_llm.TestReferrerPolicy.test_case_insensitive_lookup project_template.test_settings_llm.TestReferrerPolicy.test_default_referrer_policy_header_present project_template.test_settings_llm.TestReferrerPolicy.test_empty_middleware_no_header project_template.test_settings_llm.TestReferrerPolicy.test_global_settings_default_value project_template.test_settings_llm.TestReferrerPolicy.test_missing_security_middleware_no_header project_template.test_settings_llm.TestReferrerPolicy.test_multiple_requests_consistent_header project_template.test_settings_llm.TestReferrerPolicy.test_override_referrer_policy_to_custom_value project_template.test_settings_llm.TestReferrerPolicy.test_override_referrer_policy_to_none_removes_header project_template.test_settings_llm.TestReferrerPolicy.test_referrer_policy_header_single_entry project_template.test_settings_llm.TestReferrerPolicy.test_template_file_contains_setting project_template.test_settings_llm._parse_headers
coverage json -o coverage.json
: '>>>>> End Test Output'
