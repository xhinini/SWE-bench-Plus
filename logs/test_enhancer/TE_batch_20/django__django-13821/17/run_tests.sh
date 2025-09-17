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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.tests_llm.CheckSqliteVersionModuleReloadTests._reload_with_version backends.sqlite.tests_llm.CheckSqliteVersionModuleReloadTests.setUp backends.sqlite.tests_llm.CheckSqliteVersionModuleReloadTests.test_boundary_old_version_383_raises backends.sqlite.tests_llm.CheckSqliteVersionModuleReloadTests.test_exact_minimum_version_does_not_raise backends.sqlite.tests_llm.CheckSqliteVersionModuleReloadTests.test_longer_tuple_old_version_raises backends.sqlite.tests_llm.CheckSqliteVersionModuleReloadTests.test_major_bump_does_not_raise backends.sqlite.tests_llm.CheckSqliteVersionModuleReloadTests.test_message_reflects_sqlite_version_value backends.sqlite.tests_llm.CheckSqliteVersionModuleReloadTests.test_newer_version_does_not_raise backends.sqlite.tests_llm.CheckSqliteVersionModuleReloadTests.test_older_version_raises_with_expected_message backends.sqlite.tests_llm.CheckSqliteVersionModuleReloadTests.test_reload_sequence_old_then_new backends.sqlite.tests_llm.CheckSqliteVersionModuleReloadTests.test_short_tuple_is_considered_too_old
coverage json -o coverage.json
: '>>>>> End Test Output'
