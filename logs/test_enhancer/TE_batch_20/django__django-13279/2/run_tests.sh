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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_encode_matches__legacy_encode sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encode_decode_json_cookie_session sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encode_decode_json_cookie_session_with_unicode sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encode_decode_json_file_session sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encode_decode_pickle_cache_session sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encode_decode_pickle_cookie_session sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encode_decode_pickle_cookie_session_with_bytes sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encode_decode_pickle_file_session sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encoded_format_contains_expected_hash
coverage json -o coverage.json
: '>>>>> End Test Output'
