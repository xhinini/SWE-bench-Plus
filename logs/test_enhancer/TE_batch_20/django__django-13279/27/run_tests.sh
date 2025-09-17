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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 sessions_tests.tests_llm.LegacyEncodeRegressionTests._roundtrip sessions_tests.tests_llm.LegacyEncodeRegressionTests.test_json_list_of_unicode_roundtrip sessions_tests.tests_llm.LegacyEncodeRegressionTests.test_json_nested_unicode_and_numbers_roundtrip sessions_tests.tests_llm.LegacyEncodeRegressionTests.test_json_unicode_cafe_roundtrip sessions_tests.tests_llm.LegacyEncodeRegressionTests.test_json_unicode_cjk_roundtrip sessions_tests.tests_llm.LegacyEncodeRegressionTests.test_json_unicode_emoji_roundtrip sessions_tests.tests_llm.LegacyEncodeRegressionTests.test_json_with_timedelta_roundtrip sessions_tests.tests_llm.LegacyEncodeRegressionTests.test_pickle_bytes_value_roundtrip sessions_tests.tests_llm.LegacyEncodeRegressionTests.test_pickle_datetime_roundtrip sessions_tests.tests_llm.LegacyEncodeRegressionTests.test_pickle_large_random_bytes_roundtrip sessions_tests.tests_llm.LegacyEncodeRegressionTests.test_pickle_nested_bytes_roundtrip
coverage json -o coverage.json
: '>>>>> End Test Output'
