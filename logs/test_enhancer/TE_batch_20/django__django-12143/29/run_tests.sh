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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_changelist.tests_llm.RegexPrefixListEditableTests._make_posts_and_assert_filtered admin_changelist.tests_llm.RegexPrefixListEditableTests.setUpTestData admin_changelist.tests_llm.RegexPrefixListEditableTests.test_prefix_with_backslash admin_changelist.tests_llm.RegexPrefixListEditableTests.test_prefix_with_caret admin_changelist.tests_llm.RegexPrefixListEditableTests.test_prefix_with_dot admin_changelist.tests_llm.RegexPrefixListEditableTests.test_prefix_with_parentheses_close admin_changelist.tests_llm.RegexPrefixListEditableTests.test_prefix_with_parentheses_open admin_changelist.tests_llm.RegexPrefixListEditableTests.test_prefix_with_pipe admin_changelist.tests_llm.RegexPrefixListEditableTests.test_prefix_with_plus admin_changelist.tests_llm.RegexPrefixListEditableTests.test_prefix_with_question_mark admin_changelist.tests_llm.RegexPrefixListEditableTests.test_prefix_with_square_brackets admin_changelist.tests_llm.RegexPrefixListEditableTests.test_prefix_with_star
coverage json -o coverage.json
: '>>>>> End Test Output'
