#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
export LANG=en_US.UTF-8
export LANGUAGE=en_US:en
export LC_ALL=en_US.UTF-8
export PYTHONIOENCODING=utf8
python --version && python -m pip install -U pip
python -m pip install -U 'coverage==6.2'

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 sessions_tests.tests_llm.LegacyEncodeDatabaseBackendsTests.test_cache_db_session_legacy_encode_decode_binary_nested sessions_tests.tests_llm.LegacyEncodeDatabaseBackendsTests.test_custom_database_session_legacy_encode_decode_complex_binary sessions_tests.tests_llm.LegacyEncodeDatabaseBackendsTests.test_database_session_legacy_encode_decode_binary_value sessions_tests.tests_llm.LegacyEncodeSimpleBackendsTests.test_cache_session_legacy_encode_decode_binary_nested sessions_tests.tests_llm.LegacyEncodeSimpleBackendsTests.test_cache_session_legacy_encode_decode_deep_binary sessions_tests.tests_llm.LegacyEncodeSimpleBackendsTests.test_cookie_session_legacy_encode_decode_binary_value sessions_tests.tests_llm.LegacyEncodeSimpleBackendsTests.test_cookie_session_legacy_encode_decode_complex_binary sessions_tests.tests_llm.LegacyEncodeSimpleBackendsTests.test_file_session_legacy_encode_decode_binary_nested sessions_tests.tests_llm.LegacyEncodeSimpleBackendsTests.test_file_session_legacy_encode_decode_binary_value
coverage json -o coverage.json
: '>>>>> End Test Output'
