#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 view_tests.tests.test_static_llm.MalformedHeaderServeTests._assert_served_ok view_tests.tests.test_static_llm.MalformedHeaderServeTests.test_serve_handles_double_semicolon_header view_tests.tests.test_static_llm.MalformedHeaderServeTests.test_serve_handles_semicolon_length_header view_tests.tests.test_static_llm.MalformedHeaderServeTests.test_serve_handles_semicolon_no_space_header view_tests.tests.test_static_llm.MalformedHeaderServeTests.test_serve_handles_semicolon_only_header view_tests.tests.test_static_llm.MalformedHeaderWasModifiedTests.test_double_semicolon view_tests.tests.test_static_llm.MalformedHeaderWasModifiedTests.test_semicolon_garbage view_tests.tests.test_static_llm.MalformedHeaderWasModifiedTests.test_semicolon_length view_tests.tests.test_static_llm.MalformedHeaderWasModifiedTests.test_semicolon_no_space view_tests.tests.test_static_llm.MalformedHeaderWasModifiedTests.test_semicolon_only view_tests.tests.test_static_llm.MalformedHeaderWasModifiedTests.test_semicolon_space_only
coverage json -o coverage.json
: '>>>>> End Test Output'
