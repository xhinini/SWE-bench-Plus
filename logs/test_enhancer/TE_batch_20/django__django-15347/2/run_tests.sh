#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 messages_tests.test_cookie_llm.test_regression_cookie_roundtrip_preserves_empty_extra_tags messages_tests.test_cookie_llm.test_regression_cookie_store_restore_various_extra_tags messages_tests.test_cookie_llm.test_regression_empty_extra_tags_json messages_tests.test_cookie_llm.test_regression_empty_extra_tags_nested_structure messages_tests.test_cookie_llm.test_regression_false_extra_tags_json messages_tests.test_cookie_llm.test_regression_nested_false_extra_tags messages_tests.test_cookie_llm.test_regression_serializer_preserves_empty_extra_tags messages_tests.test_cookie_llm.test_regression_serializer_preserves_mixed_extra_tags messages_tests.test_cookie_llm.test_regression_zero_extra_tags_json
coverage json -o coverage.json
: '>>>>> End Test Output'
