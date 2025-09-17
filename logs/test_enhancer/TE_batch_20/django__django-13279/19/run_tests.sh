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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 sessions_tests.tests_llm.DummySession.create sessions_tests.tests_llm.DummySession.delete sessions_tests.tests_llm.DummySession.exists sessions_tests.tests_llm.DummySession.load sessions_tests.tests_llm.DummySession.save sessions_tests.tests_llm.LegacyEncodingTests.test_cache_session_legacy_roundtrip_binary_value sessions_tests.tests_llm.LegacyEncodingTests.test_cache_session_legacy_roundtrip_with_pickle sessions_tests.tests_llm.LegacyEncodingTests.test_cookie_session_legacy_roundtrip_with_binary_value sessions_tests.tests_llm.LegacyEncodingTests.test_cookie_session_legacy_roundtrip_with_pickle sessions_tests.tests_llm.LegacyEncodingTests.test_decode_falls_back_to_legacy_after_algorithm_change sessions_tests.tests_llm.LegacyEncodingTests.test_legacy_encode_equals__legacy_encode_for_json_serializer sessions_tests.tests_llm.LegacyEncodingTests.test_legacy_encode_uses__legacy_encode_dummy_session sessions_tests.tests_llm.LegacyEncodingTests.test_legacy_roundtrip_json_dummy_session_with_unicode sessions_tests.tests_llm.LegacyEncodingTests.test_legacy_roundtrip_pickle_dummy_session sessions_tests.tests_llm.LegacyEncodingTests.test_legacy_roundtrip_pickle_dummy_session_with_binary_value
coverage json -o coverage.json
: '>>>>> End Test Output'
