#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 view_tests.tests.test_static_llm.test_serve_with_if_modified_since_semicolon_length view_tests.tests.test_static_llm.test_serve_with_if_modified_since_semicolon_length_no_space view_tests.tests.test_static_llm.test_serve_with_if_modified_since_semicolon_non_numeric_length view_tests.tests.test_static_llm.test_serve_with_if_modified_since_semicolon_only view_tests.tests.test_static_llm.test_was_modified_since_semicolon_length view_tests.tests.test_static_llm.test_was_modified_since_semicolon_length_no_space view_tests.tests.test_static_llm.test_was_modified_since_semicolon_length_non_numeric view_tests.tests.test_static_llm.test_was_modified_since_semicolon_only view_tests.tests.test_static_llm.test_was_modified_since_semicolon_with_text
coverage json -o coverage.json
: '>>>>> End Test Output'
