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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.tests_llm.test_check_sqlite_version_3_8_11_1_raises_and_message_contains_version backends.sqlite.tests_llm.test_check_sqlite_version_3_8_3_raises backends.sqlite.tests_llm.test_check_sqlite_version_3_8_4_raises backends.sqlite.tests_llm.test_check_sqlite_version_3_8_5_raises backends.sqlite.tests_llm.test_check_sqlite_version_exact_3_9_0_ok backends.sqlite.tests_llm.test_check_sqlite_version_extra_long_tuple_ok backends.sqlite.tests_llm.test_check_sqlite_version_higher_version_ok backends.sqlite.tests_llm.test_check_sqlite_version_non_tuple_raises_typeerror backends.sqlite.tests_llm.test_check_sqlite_version_short_tuple_3_9_raises backends.sqlite.tests_llm.test_import_time_check_raises_on_old_version
coverage json -o coverage.json
: '>>>>> End Test Output'
