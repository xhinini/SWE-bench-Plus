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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 sessions_tests.tests_llm.LegacyEncodeDecodeTests.test_legacy_decode_handles_legacy_encode_direct_pickle sessions_tests.tests_llm.LegacyEncodeDecodeTests.test_legacy_encode_and_decode_with_nested_non_ascii_json sessions_tests.tests_llm.LegacyEncodeDecodeTests.test_legacy_encode_decode_non_ascii_json sessions_tests.tests_llm.LegacyEncodeDecodeTests.test_legacy_encode_decode_unicode_key_and_value_json sessions_tests.tests_llm.LegacyEncodeDecodeTests.test_legacy_encode_decode_with_pickle_serializer_binary_value sessions_tests.tests_llm.LegacyEncodeDecodeTests.test_legacy_encode_outputs_base64_and_hash_prefix_pickle sessions_tests.tests_llm.LegacyEncodeDecodeTests.test_legacy_encode_preserves_unicode_keys_json sessions_tests.tests_llm.LegacyEncodeDecodeTests.test_legacy_encode_then_legacy_decode_roundtrip_json sessions_tests.tests_llm.LegacyEncodeDecodeTests.test_multiple_legacy_roundtrips_pickle sessions_tests.tests_llm.LegacyEncodeDecodeTests.test_non_sha_algorithm_handles_non_ascii_json
coverage json -o coverage.json
: '>>>>> End Test Output'
