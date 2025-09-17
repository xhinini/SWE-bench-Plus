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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 sessions_tests.tests_llm.DummySession.clear_expired sessions_tests.tests_llm.DummySession.create sessions_tests.tests_llm.DummySession.delete sessions_tests.tests_llm.DummySession.exists sessions_tests.tests_llm.DummySession.load sessions_tests.tests_llm.DummySession.save sessions_tests.tests_llm.LegacyEncodePickleTests.setUp sessions_tests.tests_llm.LegacyEncodePickleTests.test_legacy_encode_roundtrip_via_decode_api sessions_tests.tests_llm.LegacyEncodePickleTests.test_legacy_encode_with_bytearray sessions_tests.tests_llm.LegacyEncodePickleTests.test_legacy_encode_with_bytes_value sessions_tests.tests_llm.LegacyEncodePickleTests.test_legacy_encode_with_large_binary_blob sessions_tests.tests_llm.LegacyEncodePickleTests.test_legacy_encode_with_memoryview sessions_tests.tests_llm.LegacyEncodePickleTests.test_legacy_encode_with_nested_bytes sessions_tests.tests_llm.LegacyEncodePickleTests.test_legacy_encode_with_non_ascii_in_key_and_value sessions_tests.tests_llm.LegacyEncodePickleTests.test_legacy_encode_with_null_byte_in_bytes sessions_tests.tests_llm.LegacyEncodePickleTests.test_legacy_encode_with_set_of_bytes sessions_tests.tests_llm.LegacyEncodePickleTests.test_legacy_encode_with_tuple_of_bytes
coverage json -o coverage.json
: '>>>>> End Test Output'
