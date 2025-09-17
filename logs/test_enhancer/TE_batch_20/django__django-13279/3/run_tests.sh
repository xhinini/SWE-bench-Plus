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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 sessions_tests.tests_llm.LegacyEncodeDecodePickleTests.test_legacy__legacy_decode_direct sessions_tests.tests_llm.LegacyEncodeDecodePickleTests.test_legacy_encoded_is_ascii_string sessions_tests.tests_llm.LegacyEncodeDecodePickleTests.test_legacy_roundtrip_pickle_bytearray sessions_tests.tests_llm.LegacyEncodeDecodePickleTests.test_legacy_roundtrip_pickle_bytes sessions_tests.tests_llm.LegacyEncodeDecodePickleTests.test_legacy_roundtrip_pickle_datetime sessions_tests.tests_llm.LegacyEncodeDecodePickleTests.test_legacy_roundtrip_pickle_large_binary sessions_tests.tests_llm.LegacyEncodeDecodePickleTests.test_legacy_roundtrip_pickle_nested_bytes sessions_tests.tests_llm.LegacyEncodeDecodePickleTests.test_legacy_roundtrip_pickle_non_ascii_unicode sessions_tests.tests_llm.LegacyEncodeDecodePickleTests.test_legacy_roundtrip_pickle_null_byte sessions_tests.tests_llm.LegacyEncodeDecodePickleTests.test_non_legacy_roundtrip_pickle_bytes
coverage json -o coverage.json
: '>>>>> End Test Output'
