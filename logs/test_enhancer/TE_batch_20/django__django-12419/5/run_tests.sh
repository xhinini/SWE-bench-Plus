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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 project_template.test_settings_llm.TestReferrerPolicy._headers_dict project_template.test_settings_llm.TestReferrerPolicy.setUp project_template.test_settings_llm.TestReferrerPolicy.test_default_referrer_policy_present project_template.test_settings_llm.TestReferrerPolicy.test_no_header_if_security_middleware_missing project_template.test_settings_llm.TestReferrerPolicy.test_referrer_policy_consistent_across_multiple_requests project_template.test_settings_llm.TestReferrerPolicy.test_referrer_policy_empty_string_not_present project_template.test_settings_llm.TestReferrerPolicy.test_referrer_policy_header_single_instance project_template.test_settings_llm.TestReferrerPolicy.test_referrer_policy_no_referrer project_template.test_settings_llm.TestReferrerPolicy.test_referrer_policy_none_not_present project_template.test_settings_llm.TestReferrerPolicy.test_referrer_policy_origin project_template.test_settings_llm.TestReferrerPolicy.test_referrer_policy_unsafe_url project_template.test_settings_llm.TestReferrerPolicy.test_referrer_policy_value_is_text
coverage json -o coverage.json
: '>>>>> End Test Output'
