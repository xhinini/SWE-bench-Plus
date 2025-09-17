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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 sessions_tests.tests_llm.LegacyPickleEncodingCookieTests.test_cookie_session_legacy_encode_roundtrip sessions_tests.tests_llm.LegacyPickleEncodingCookieTests.test_cookie_session_legacy_encode_with_non_ascii_pickled_bytes sessions_tests.tests_llm.LegacyPickleEncodingDatabaseTests.test_database_session_legacy_encode_roundtrip sessions_tests.tests_llm.LegacyPickleEncodingDatabaseTests.test_database_session_legacy_encode_with_bytes_value sessions_tests.tests_llm.LegacyPickleEncodingDatabaseTests.test_database_session_multiple_roundtrips sessions_tests.tests_llm.LegacyPickleEncodingSimpleBackendsTests.test_cache_session_legacy_encode_roundtrip sessions_tests.tests_llm.LegacyPickleEncodingSimpleBackendsTests.test_cached_db_session_legacy_encode_roundtrip sessions_tests.tests_llm.LegacyPickleEncodingSimpleBackendsTests.test_file_session_legacy_encode_roundtrip
coverage json -o coverage.json
: '>>>>> End Test Output'
