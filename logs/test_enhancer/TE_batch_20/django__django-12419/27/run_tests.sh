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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 project_template.test_settings_llm.test_custom_string_referrer_policy_is_used project_template.test_settings_llm.test_default_referrer_policy_header_present_by_default project_template.test_settings_llm.test_empty_string_sets_empty_referrer_policy_header project_template.test_settings_llm.test_explicit_none_disables_referrer_policy_header project_template.test_settings_llm.test_multiple_requests_consistently_set_referrer_policy project_template.test_settings_llm.test_no_security_middleware_no_referrer_policy_header_even_if_setting_present project_template.test_settings_llm.test_numeric_referrer_policy_is_coerced_to_string project_template.test_settings_llm.test_project_template_settings_middleware_produces_referrer_policy project_template.test_settings_llm.test_security_middleware_at_end_still_sets_header
coverage json -o coverage.json
: '>>>>> End Test Output'
