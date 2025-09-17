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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 sessions_tests.tests_llm.LegacySessionEncodingTests.test_legacy_decode_rejects_tampered_hash_and_logs sessions_tests.tests_llm.LegacySessionEncodingTests.test_legacy_encode_bytes_roundtrip sessions_tests.tests_llm.LegacySessionEncodingTests.test_legacy_encode_does_not_raise_unicode_decode_error sessions_tests.tests_llm.LegacySessionEncodingTests.test_legacy_encode_large_binary_roundtrip sessions_tests.tests_llm.LegacySessionEncodingTests.test_legacy_encode_preserves_nested_bytes sessions_tests.tests_llm.LegacySessionEncodingTests.test_legacy_encode_unicode_roundtrip sessions_tests.tests_llm.LegacySessionEncodingTests.test_legacy_encode_with_custom_serializer_bytes_payload sessions_tests.tests_llm.LegacySessionEncodingTests.test_legacy_encoded_is_valid_base64_with_hash_and_serialized sessions_tests.tests_llm.LegacySessionEncodingTests.test_legacy_roundtrip_with_mixed_types sessions_tests.tests_llm.LegacySessionEncodingTests.test_non_legacy_encode_roundtrip_when_algo_not_sha1
coverage json -o coverage.json
: '>>>>> End Test Output'
