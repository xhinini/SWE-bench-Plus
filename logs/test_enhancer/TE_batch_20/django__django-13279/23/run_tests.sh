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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 sessions_tests.tests_llm.LegacyEncodeNonAsciiTests._roundtrip sessions_tests.tests_llm.LegacyEncodeNonAsciiTests.test_cache_session_non_ascii_payload sessions_tests.tests_llm.LegacyEncodeNonAsciiTests.test_cachedb_session_non_ascii_payload sessions_tests.tests_llm.LegacyEncodeNonAsciiTests.test_cookie_session_non_ascii_payload sessions_tests.tests_llm.LegacyEncodeNonAsciiTests.test_custom_database_session_non_ascii_payload sessions_tests.tests_llm.LegacyEncodeNonAsciiTests.test_database_session_large_non_ascii_payload sessions_tests.tests_llm.LegacyEncodeNonAsciiTests.test_database_session_mixed_types_non_ascii_payload sessions_tests.tests_llm.LegacyEncodeNonAsciiTests.test_database_session_nested_non_ascii_payload sessions_tests.tests_llm.LegacyEncodeNonAsciiTests.test_database_session_non_ascii_payload sessions_tests.tests_llm.LegacyEncodeNonAsciiTests.test_database_session_non_ascii_with_zero_byte sessions_tests.tests_llm.LegacyEncodeNonAsciiTests.test_file_session_non_ascii_payload sessions_tests.tests_llm.NonAsciiBytesSerializer.dumps sessions_tests.tests_llm.NonAsciiBytesSerializer.loads
coverage json -o coverage.json
: '>>>>> End Test Output'
