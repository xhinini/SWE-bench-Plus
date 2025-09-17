#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 view_tests.tests.test_static_llm.WasModifiedSinceMalformedHeaderTests.test_double_semicolon_sequence view_tests.tests.test_static_llm.WasModifiedSinceMalformedHeaderTests.test_leading_semicolon_multiple_digits view_tests.tests.test_static_llm.WasModifiedSinceMalformedHeaderTests.test_leading_semicolon_with_length view_tests.tests.test_static_llm.WasModifiedSinceMalformedHeaderTests.test_leading_semicolon_zero_length view_tests.tests.test_static_llm.WasModifiedSinceMalformedHeaderTests.test_missing_space_after_semicolon_length_keyword view_tests.tests.test_static_llm.WasModifiedSinceMalformedHeaderTests.test_semicolon_and_space_only view_tests.tests.test_static_llm.WasModifiedSinceMalformedHeaderTests.test_semicolon_followed_by_garbage view_tests.tests.test_static_llm.WasModifiedSinceMalformedHeaderTests.test_valid_date_but_invalid_length_token
coverage json -o coverage.json
: '>>>>> End Test Output'
