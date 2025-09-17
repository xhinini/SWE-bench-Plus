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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 project_template.test_settings_llm.TestReferrerPolicyRegression._get_referrer_policy_header project_template.test_settings_llm.TestReferrerPolicyRegression.setUp project_template.test_settings_llm.TestReferrerPolicyRegression.test_empty_string_setting_produces_header_with_empty_value project_template.test_settings_llm.TestReferrerPolicyRegression.test_whitespace_value_preserved_exactly
coverage json -o coverage.json
: '>>>>> End Test Output'
