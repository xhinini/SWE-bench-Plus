#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 validators.tests_llm.TestURLValidatorCustomUnsafeChars.assert_unsafe_char_rejected validators.tests_llm.TestURLValidatorCustomUnsafeChars.test_caret_in_path validators.tests_llm.TestURLValidatorCustomUnsafeChars.test_caret_in_userinfo validators.tests_llm.TestURLValidatorCustomUnsafeChars.test_pipe_in_fragment validators.tests_llm.TestURLValidatorCustomUnsafeChars.test_pipe_in_path validators.tests_llm.TestURLValidatorCustomUnsafeChars.test_pipe_in_query validators.tests_llm.TestURLValidatorCustomUnsafeChars.test_pipe_in_userinfo validators.tests_llm.TestURLValidatorCustomUnsafeChars.test_semicolon_in_fragment validators.tests_llm.TestURLValidatorCustomUnsafeChars.test_semicolon_in_path validators.tests_llm.TestURLValidatorCustomUnsafeChars.test_semicolon_in_query validators.tests_llm.TestURLValidatorCustomUnsafeChars.test_semicolon_in_userinfo
coverage json -o coverage.json
: '>>>>> End Test Output'
