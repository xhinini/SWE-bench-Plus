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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.tests_llm.SQLiteVersionCheckTests._attempt_import backends.sqlite.tests_llm.SQLiteVersionCheckTests._import_base_with_version backends.sqlite.tests_llm.SQLiteVersionCheckTests.test_allows_3_10_0 backends.sqlite.tests_llm.SQLiteVersionCheckTests.test_allows_3_9_0 backends.sqlite.tests_llm.SQLiteVersionCheckTests.test_allows_3_9_1 backends.sqlite.tests_llm.SQLiteVersionCheckTests.test_allows_4_0_0 backends.sqlite.tests_llm.SQLiteVersionCheckTests.test_exception_message_includes_version backends.sqlite.tests_llm.SQLiteVersionCheckTests.test_raises_for_3_5_0 backends.sqlite.tests_llm.SQLiteVersionCheckTests.test_raises_for_3_8_11_1 backends.sqlite.tests_llm.SQLiteVersionCheckTests.test_raises_for_3_8_3_exact backends.sqlite.tests_llm.SQLiteVersionCheckTests.test_raises_for_3_8_99 backends.sqlite.tests_llm.SQLiteVersionCheckTests.test_successful_import_exposes_DatabaseWrapper
coverage json -o coverage.json
: '>>>>> End Test Output'
