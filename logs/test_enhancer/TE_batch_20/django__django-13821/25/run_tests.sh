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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.tests_llm.AdditionalCheckSQLiteVersionTests.test_3_8_4_raises backends.sqlite.tests_llm.AdditionalCheckSQLiteVersionTests.test_exact_3_9_0_does_not_raise backends.sqlite.tests_llm.AdditionalCheckSQLiteVersionTests.test_four_tuple_with_patch_passes backends.sqlite.tests_llm.AdditionalCheckSQLiteVersionTests.test_higher_version_does_not_raise backends.sqlite.tests_llm.AdditionalCheckSQLiteVersionTests.test_lower_version_3_8_3_raises backends.sqlite.tests_llm.AdditionalCheckSQLiteVersionTests.test_lower_version_with_four_tuple_raises backends.sqlite.tests_llm.AdditionalCheckSQLiteVersionTests.test_major_version_lower_raises backends.sqlite.tests_llm.AdditionalCheckSQLiteVersionTests.test_message_exact_text_for_lower_version backends.sqlite.tests_llm.AdditionalCheckSQLiteVersionTests.test_multiple_calls_different_versions backends.sqlite.tests_llm.AdditionalCheckSQLiteVersionTests.test_short_tuple_like_3_9_raises
coverage json -o coverage.json
: '>>>>> End Test Output'
