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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 sessions_tests.tests_llm.LegacyEncodingDBRegressionTests.test_legacy_encode_roundtrip_via_legacy_methods_json sessions_tests.tests_llm.LegacyEncodingDBRegressionTests.test_legacy_encode_roundtrip_via_legacy_methods_pickle sessions_tests.tests_llm.LegacyEncodingDBRegressionTests.test_sha1_json_unicode_database_roundtrip sessions_tests.tests_llm.LegacyEncodingDBRegressionTests.test_sha1_pickle_unicode_database_roundtrip sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_sha1_json_unicode_cookie_encode_returns_str sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_sha1_json_unicode_cookie_roundtrip sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_sha1_pickle_unicode_cookie_encode_returns_str sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_sha1_pickle_unicode_cookie_roundtrip sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_switching_algorithm_decodes_legacy_session_json sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_switching_algorithm_decodes_legacy_session_pickle
coverage json -o coverage.json
: '>>>>> End Test Output'
