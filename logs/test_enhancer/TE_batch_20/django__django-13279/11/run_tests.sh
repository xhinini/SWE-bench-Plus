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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 sessions_tests.tests_llm.LegacyEncodingRegressionTests.setUp sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_encode_produces_base64_with_colon_and_sha1_hash_length sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_decode_logs_on_corrupted_data_sha1 sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encode_handles_empty_dict sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encode_json_serializer_decodes sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encode_json_serializer_non_ascii sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encode_pickle_serializer_decodes sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encode_pickle_serializer_non_ascii sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encode_with_custom_serializer_returning_bytes sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encode_with_custom_serializer_returning_str sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_session_decode_roundtrip_calls_legacy_decoder
coverage json -o coverage.json
: '>>>>> End Test Output'
