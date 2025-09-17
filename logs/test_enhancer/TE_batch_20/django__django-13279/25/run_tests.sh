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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_decode_legacy_via_decode_method sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_encode_does_not_raise_for_json_serializer_with_unicode sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_encode_does_not_raise_for_pickle_serializer_with_binary sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_json_serializer_legacy_encode_decode_roundtrip sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_json_serializer_unicode_legacy_encode_decode_roundtrip sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encode_and__legacy_decode_consistent sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_encoded_format_has_hash_and_serialized_part sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_legacy_hash_matches_internal_hash_computation sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_pickle_serializer_legacy_encode_decode_roundtrip sessions_tests.tests_llm.LegacyEncodingRegressionTests.test_roundtrip_complex_structure_pickle
coverage json -o coverage.json
: '>>>>> End Test Output'
