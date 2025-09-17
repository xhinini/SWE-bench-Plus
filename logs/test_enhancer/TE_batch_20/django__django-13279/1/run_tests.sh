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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 sessions_tests.tests_llm.LegacyEncodeDecodeTests.test_legacy_json_empty_dict sessions_tests.tests_llm.LegacyEncodeDecodeTests.test_legacy_json_nested sessions_tests.tests_llm.LegacyEncodeDecodeTests.test_legacy_json_numeric_types sessions_tests.tests_llm.LegacyEncodeDecodeTests.test_legacy_json_simple_unicode sessions_tests.tests_llm.LegacyEncodeDecodeTests.test_legacy_pickle_binary_simple sessions_tests.tests_llm.LegacyEncodeDecodeTests.test_legacy_pickle_full_byte_range sessions_tests.tests_llm.LegacyEncodeDecodeTests.test_legacy_pickle_list_with_bytes sessions_tests.tests_llm.LegacyEncodeDecodeTests.test_legacy_pickle_nested_binary sessions_tests.tests_llm.LegacyEncodeDecodeTests.test_legacy_pickle_none_and_bytes sessions_tests.tests_llm.LegacyEncodeDecodeTests.test_legacy_pickle_unicode_value
coverage json -o coverage.json
: '>>>>> End Test Output'
