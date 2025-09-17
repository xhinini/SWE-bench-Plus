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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_encode_equals_legacy_encode_pickle sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_encode_roundtrip_using_different_instances sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_encode_with_binary_value_pickle sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_encode_with_non_ascii_data_pickle sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_json_serializer_encode_decode_sha1 sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encode_not_throw_on_pickle_bytes sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encoded_cookie_decodes_after_changing_algorithm sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encoded_decodes_after_switching_hash_algorithm sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_pickle_serializer_encode_decode_sha1_cookie sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_pickle_serializer_encode_decode_sha1_database
coverage json -o coverage.json
: '>>>>> End Test Output'
