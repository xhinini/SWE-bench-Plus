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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.tests_llm.CheckSQLiteVersionAdditionalTests.test_import_time_no_raise_when_new backends.sqlite.tests_llm.CheckSQLiteVersionAdditionalTests.test_import_time_raises_when_old backends.sqlite.tests_llm.CheckSQLiteVersionAdditionalTests.test_message_includes_full_version_string backends.sqlite.tests_llm.CheckSQLiteVersionAdditionalTests.test_no_raise_for_exact_3_9_0 backends.sqlite.tests_llm.CheckSQLiteVersionAdditionalTests.test_no_raise_for_newer_version backends.sqlite.tests_llm.CheckSQLiteVersionAdditionalTests.test_raises_for_3_8_3 backends.sqlite.tests_llm.CheckSQLiteVersionAdditionalTests.test_raises_for_3_8_99 backends.sqlite.tests_llm.CheckSQLiteVersionAdditionalTests.test_short_tuple_raises backends.sqlite.tests_llm.CheckSQLiteVersionAdditionalTests.test_tuple_with_extra_components_above_boundary
coverage json -o coverage.json
: '>>>>> End Test Output'
