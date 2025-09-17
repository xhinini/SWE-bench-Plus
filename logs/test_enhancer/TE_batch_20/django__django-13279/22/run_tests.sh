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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 sessions_tests.tests_llm.LegacySessionEncodingTests.test_decode_legacy_after_algorithm_switch_preserves_serializer sessions_tests.tests_llm.LegacySessionEncodingTests.test_legacy_encode_does_not_raise_unicode_error_for_json sessions_tests.tests_llm.LegacySessionEncodingTests.test_legacy_encode_returns_str_type_for_pickle sessions_tests.tests_llm.LegacySessionEncodingTests.test_legacy_json_emoji_roundtrip sessions_tests.tests_llm.LegacySessionEncodingTests.test_legacy_json_large_unicode_roundtrip sessions_tests.tests_llm.LegacySessionEncodingTests.test_legacy_json_nested_unicode_roundtrip sessions_tests.tests_llm.LegacySessionEncodingTests.test_legacy_json_unicode_key_roundtrip sessions_tests.tests_llm.LegacySessionEncodingTests.test_legacy_json_unicode_roundtrip sessions_tests.tests_llm.LegacySessionEncodingTests.test_legacy_pickle_binary_roundtrip sessions_tests.tests_llm.LegacySessionEncodingTests.test_legacy_pickle_non_ascii_bytes_roundtrip
coverage json -o coverage.json
: '>>>>> End Test Output'
