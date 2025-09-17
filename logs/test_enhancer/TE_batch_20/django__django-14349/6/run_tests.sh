#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 validators.tests_llm.URLValidatorCustomUnsafeCharsTests.test_backtick_in_path validators.tests_llm.URLValidatorCustomUnsafeCharsTests.test_caret_in_fragment validators.tests_llm.URLValidatorCustomUnsafeCharsTests.test_custom_unsafe_char_in_userinfo_and_path validators.tests_llm.URLValidatorCustomUnsafeCharsTests.test_emoji_in_path validators.tests_llm.URLValidatorCustomUnsafeCharsTests.test_multiple_custom_unsafe_chars validators.tests_llm.URLValidatorCustomUnsafeCharsTests.test_percent_in_path validators.tests_llm.URLValidatorCustomUnsafeCharsTests.test_pipe_in_path validators.tests_llm.URLValidatorCustomUnsafeCharsTests.test_pipe_in_userinfo validators.tests_llm.URLValidatorCustomUnsafeCharsTests.test_plus_in_path validators.tests_llm.URLValidatorCustomUnsafeCharsTests.test_semicolon_in_path
coverage json -o coverage.json
: '>>>>> End Test Output'
