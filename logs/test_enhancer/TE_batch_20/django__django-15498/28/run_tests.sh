#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 view_tests.tests.test_static_llm.test_serve_handles_header_with_extra_param view_tests.tests.test_static_llm.test_serve_handles_invalid_length_in_header view_tests.tests.test_static_llm.test_serve_handles_leading_semicolon_token view_tests.tests.test_static_llm.test_serve_handles_multiple_semicolons view_tests.tests.test_static_llm.test_serve_handles_trailing_garbage_after_length view_tests.tests.test_static_llm.test_was_modified_since_extra_semicolon_token view_tests.tests.test_static_llm.test_was_modified_since_invalid_length_token view_tests.tests.test_static_llm.test_was_modified_since_leading_semicolon_token view_tests.tests.test_static_llm.test_was_modified_since_multiple_semicolons view_tests.tests.test_static_llm.test_was_modified_since_trailing_garbage_after_length
coverage json -o coverage.json
: '>>>>> End Test Output'
