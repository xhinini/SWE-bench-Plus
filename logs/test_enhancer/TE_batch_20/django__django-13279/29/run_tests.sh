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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 sessions_tests.tests_llm.LegacyEncodePickleSerializerTests.roundtrip sessions_tests.tests_llm.LegacyEncodePickleSerializerTests.setUp sessions_tests.tests_llm.LegacyEncodePickleSerializerTests.test_bytes_only_value sessions_tests.tests_llm.LegacyEncodePickleSerializerTests.test_bytes_value sessions_tests.tests_llm.LegacyEncodePickleSerializerTests.test_empty_dict sessions_tests.tests_llm.LegacyEncodePickleSerializerTests.test_large_payload sessions_tests.tests_llm.LegacyEncodePickleSerializerTests.test_mixed_key_types sessions_tests.tests_llm.LegacyEncodePickleSerializerTests.test_nested_structure sessions_tests.tests_llm.LegacyEncodePickleSerializerTests.test_none_and_bool sessions_tests.tests_llm.LegacyEncodePickleSerializerTests.test_simple_dict sessions_tests.tests_llm.LegacyEncodePickleSerializerTests.test_tuple_and_bytes sessions_tests.tests_llm.LegacyEncodePickleSerializerTests.test_unicode_string
coverage json -o coverage.json
: '>>>>> End Test Output'
