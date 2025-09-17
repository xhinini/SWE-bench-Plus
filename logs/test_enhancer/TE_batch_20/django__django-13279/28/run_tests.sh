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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 sessions_tests.tests_llm.CustomBinarySerializer.dumps sessions_tests.tests_llm.CustomBinarySerializer.loads sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_custom_binary_serializer_roundtrip sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_decode_falls_back_to_legacy_after_signing_failure sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encode_contains_hash_and_serialized_parts sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encode_large_binary_blob_roundtrip sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encode_pickle_nested_structures sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encode_pickle_simple sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encode_pickle_unicode_value sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encode_pickle_with_binary_blob sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encode_repeated_calls_consistent sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encode_with_non_ascii_bytes_value
coverage json -o coverage.json
: '>>>>> End Test Output'
