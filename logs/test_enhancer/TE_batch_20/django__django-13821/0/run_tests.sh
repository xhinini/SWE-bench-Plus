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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.tests_llm.SQLiteBackendVersionAndUtilsTests.test_check_sqlite_version_message_contains_full_version_string backends.sqlite.tests_llm.SQLiteBackendVersionAndUtilsTests.test_check_sqlite_version_passes_on_3_9_0 backends.sqlite.tests_llm.SQLiteBackendVersionAndUtilsTests.test_check_sqlite_version_passes_on_newer_version backends.sqlite.tests_llm.SQLiteBackendVersionAndUtilsTests.test_check_sqlite_version_raises_on_3_8_3 backends.sqlite.tests_llm.SQLiteBackendVersionAndUtilsTests.test_check_sqlite_version_raises_on_3_8_4 backends.sqlite.tests_llm.SQLiteBackendVersionAndUtilsTests.test_convert_query_multiple_placeholders_and_escapes backends.sqlite.tests_llm.SQLiteBackendVersionAndUtilsTests.test_convert_query_percent_handling_literal_and_placeholder backends.sqlite.tests_llm.SQLiteBackendVersionAndUtilsTests.test_format_dtdelta_plus_minus_and_invalid_inputs backends.sqlite.tests_llm.SQLiteBackendVersionAndUtilsTests.test_time_diff_microseconds backends.sqlite.tests_llm.SQLiteBackendVersionAndUtilsTests.test_timestamp_diff_microseconds
coverage json -o coverage.json
: '>>>>> End Test Output'
