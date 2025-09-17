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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.tests_llm.CheckSQLiteVersionBoundaryTests._import_with_version backends.sqlite.tests_llm.CheckSQLiteVersionBoundaryTests.test_check_function_behavior_when_called_directly backends.sqlite.tests_llm.CheckSQLiteVersionBoundaryTests.test_message_uses_sqlite_version_string backends.sqlite.tests_llm.CheckSQLiteVersionBoundaryTests.test_rejects_3_8_11_1_matches_existing_message backends.sqlite.tests_llm.CheckSQLiteVersionBoundaryTests.test_rejects_3_8_2 backends.sqlite.tests_llm.CheckSQLiteVersionBoundaryTests.test_rejects_3_8_3 backends.sqlite.tests_llm.CheckSQLiteVersionBoundaryTests.test_rejects_short_tuple_versions
coverage json -o coverage.json
: '>>>>> End Test Output'
