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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_encode_does_not_raise_attribute_error_with_json_db sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_encode_does_not_raise_unicode_error_with_pickle_db sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_json_serializer_sha1_cache_encode_decode sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_json_serializer_sha1_cookie_encode_decode sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_json_serializer_sha1_database_encode_decode sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_pickle_serializer_sha1_cache_encode_decode sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_pickle_serializer_sha1_cookie_encode_decode sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_pickle_serializer_sha1_database_encode_decode sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_roundtrip_legacy_encoded_string_with_json_db sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_roundtrip_legacy_encoded_string_with_pickle_db
coverage json -o coverage.json
: '>>>>> End Test Output'
