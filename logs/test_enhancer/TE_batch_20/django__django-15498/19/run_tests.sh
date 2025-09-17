#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 view_tests.tests.test_static_llm.SemicolonHeaderTests._read_file view_tests.tests.test_static_llm.SemicolonHeaderTests.test_serve_with_double_semicolon_header view_tests.tests.test_static_llm.SemicolonHeaderTests.test_serve_with_leading_semicolon_and_date_header view_tests.tests.test_static_llm.SemicolonHeaderTests.test_serve_with_semicolon_length_header view_tests.tests.test_static_llm.SemicolonHeaderTests.test_serve_with_single_semicolon_header view_tests.tests.test_static_llm.SemicolonHeaderTests.test_was_modified_since_double_semicolon view_tests.tests.test_static_llm.SemicolonHeaderTests.test_was_modified_since_leading_semicolon_and_date view_tests.tests.test_static_llm.SemicolonHeaderTests.test_was_modified_since_semicolon_length_mismatch view_tests.tests.test_static_llm.SemicolonHeaderTests.test_was_modified_since_single_semicolon view_tests.tests.test_static_llm.SemicolonHeaderTests.test_was_modified_since_single_semicolon_with_length
coverage json -o coverage.json
: '>>>>> End Test Output'
