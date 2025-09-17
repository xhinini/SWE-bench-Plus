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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 sessions_tests.tests_llm.LegacySha1EncodingTests.setUp sessions_tests.tests_llm.LegacySha1EncodingTests.test_legacy_encode_empty_bytes sessions_tests.tests_llm.LegacySha1EncodingTests.test_legacy_encode_large_binary_payload sessions_tests.tests_llm.LegacySha1EncodingTests.test_legacy_encode_mixed_types sessions_tests.tests_llm.LegacySha1EncodingTests.test_legacy_encode_non_ascii_keys sessions_tests.tests_llm.LegacySha1EncodingTests.test_legacy_encode_null_byte_in_value sessions_tests.tests_llm.LegacySha1EncodingTests.test_legacy_encode_pickle_bytes_value sessions_tests.tests_llm.LegacySha1EncodingTests.test_legacy_encode_pickle_nested_binary sessions_tests.tests_llm.LegacySha1EncodingTests.test_legacy_encode_pickle_non_ascii_unicode_value sessions_tests.tests_llm.LegacySha1EncodingTests.test_legacy_encode_with_custom_binary_prefixed_serializer sessions_tests.tests_llm.LegacySha1EncodingTests.test_legacy_encoded_payload_structure_and_roundtrip
coverage json -o coverage.json
: '>>>>> End Test Output'
