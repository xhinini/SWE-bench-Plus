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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 sessions_tests.tests_llm.LegacyEncodingRegressionTests.setUp sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_decode_works_even_if_default_hashing_algorithm_changed_after_encode sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encode_does_not_raise_unicode_error sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encode_handles_large_binary_payload sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encode_pickle_roundtrip sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encode_preserves_null_bytes sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encode_with_json_serializer_ascii_data sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encode_with_non_string_keys_and_binary_values sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encode_with_timedelta_and_binary sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encoded_blob_starts_with_sha1_hash_and_colon
coverage json -o coverage.json
: '>>>>> End Test Output'
