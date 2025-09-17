#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 view_tests.tests.test_static_llm.WasModifiedSinceMalformedHeaderTests.test_empty_length_token view_tests.tests.test_static_llm.WasModifiedSinceMalformedHeaderTests.test_leading_semicolons_then_length view_tests.tests.test_static_llm.WasModifiedSinceMalformedHeaderTests.test_multiple_semicolons_before_length view_tests.tests.test_static_llm.WasModifiedSinceMalformedHeaderTests.test_no_space_before_length_token view_tests.tests.test_static_llm.WasModifiedSinceMalformedHeaderTests.test_non_digit_length_value view_tests.tests.test_static_llm.WasModifiedSinceMalformedHeaderTests.test_only_garbage_semicolons view_tests.tests.test_static_llm.WasModifiedSinceMalformedHeaderTests.test_only_semicolon view_tests.tests.test_static_llm.WasModifiedSinceMalformedHeaderTests.test_semicolon_and_tab_before_length view_tests.tests.test_static_llm.WasModifiedSinceMalformedHeaderTests.test_semicolon_prefix_length
coverage json -o coverage.json
: '>>>>> End Test Output'
