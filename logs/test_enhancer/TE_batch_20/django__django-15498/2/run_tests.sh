#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 view_tests.tests.test_static_llm.test_serve_with_malformed_if_modified_since_only_semicolon view_tests.tests.test_static_llm.test_serve_with_malformed_if_modified_since_semicolon view_tests.tests.test_static_llm.test_was_modified_since_header_no_space_after_semicolon view_tests.tests.test_static_llm.test_was_modified_since_header_non_digit_length view_tests.tests.test_static_llm.test_was_modified_since_header_only_semicolon view_tests.tests.test_static_llm.test_was_modified_since_header_semicolon_with_spaces_only view_tests.tests.test_static_llm.test_was_modified_since_header_starts_with_semicolon view_tests.tests.test_static_llm.test_was_modified_since_header_starts_with_semicolon_size_mismatch view_tests.tests.test_static_llm.test_was_modified_since_valid_date_with_length_mismatch view_tests.tests.test_static_llm.test_was_modified_since_valid_date_with_matching_length
coverage json -o coverage.json
: '>>>>> End Test Output'
