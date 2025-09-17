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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 sessions_tests.tests_llm.LegacyEncodeRegressionTests.test_legacy__legacy_decode_direct_call sessions_tests.tests_llm.LegacyEncodeRegressionTests.test_legacy_encode_decode_large_payload sessions_tests.tests_llm.LegacyEncodeRegressionTests.test_legacy_encode_decode_mixed_types sessions_tests.tests_llm.LegacyEncodeRegressionTests.test_legacy_encode_decode_pickle_empty_bytes_and_strings sessions_tests.tests_llm.LegacyEncodeRegressionTests.test_legacy_encode_decode_pickle_nested_structures sessions_tests.tests_llm.LegacyEncodeRegressionTests.test_legacy_encode_decode_pickle_non_ascii_key sessions_tests.tests_llm.LegacyEncodeRegressionTests.test_legacy_encode_decode_pickle_non_ascii_value sessions_tests.tests_llm.LegacyEncodeRegressionTests.test_legacy_encode_decode_pickle_simple_ascii sessions_tests.tests_llm.LegacyEncodeRegressionTests.test_legacy_encode_decode_pickle_with_binary_value sessions_tests.tests_llm.LegacyEncodeRegressionTests.test_legacy_encode_decode_pickle_with_emoji
coverage json -o coverage.json
: '>>>>> End Test Output'
