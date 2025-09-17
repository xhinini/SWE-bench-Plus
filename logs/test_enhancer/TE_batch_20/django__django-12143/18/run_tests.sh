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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_changelist.tests_llm.RegexPrefixPKNameTests._run_case admin_changelist.tests_llm.RegexPrefixPKNameTests.setUpTestData admin_changelist.tests_llm.RegexPrefixPKNameTests.test_regex_prefix_case_10_mixed admin_changelist.tests_llm.RegexPrefixPKNameTests.test_regex_prefix_case_1_dollar admin_changelist.tests_llm.RegexPrefixPKNameTests.test_regex_prefix_case_2_brackets admin_changelist.tests_llm.RegexPrefixPKNameTests.test_regex_prefix_case_3_dot admin_changelist.tests_llm.RegexPrefixPKNameTests.test_regex_prefix_case_4_plus admin_changelist.tests_llm.RegexPrefixPKNameTests.test_regex_prefix_case_5_star admin_changelist.tests_llm.RegexPrefixPKNameTests.test_regex_prefix_case_6_paren admin_changelist.tests_llm.RegexPrefixPKNameTests.test_regex_prefix_case_7_question admin_changelist.tests_llm.RegexPrefixPKNameTests.test_regex_prefix_case_8_caret admin_changelist.tests_llm.RegexPrefixPKNameTests.test_regex_prefix_case_9_hyphen_dot
coverage json -o coverage.json
: '>>>>> End Test Output'
