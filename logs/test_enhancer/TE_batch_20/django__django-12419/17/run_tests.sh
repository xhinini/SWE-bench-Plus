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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 project_template.test_settings_llm.TestReferrerPolicy._count_referrer_policy_header project_template.test_settings_llm.TestReferrerPolicy._get_referrer_policy_from_response project_template.test_settings_llm.TestReferrerPolicy.setUp project_template.test_settings_llm.TestReferrerPolicy.test_switching_between_values_reflects_in_header project_template.test_settings_llm.TestReferrerPolicy.test_whitespace_value_preserved_in_header
coverage json -o coverage.json
: '>>>>> End Test Output'
