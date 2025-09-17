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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.tests_llm.CheckSQLiteVersionExtraTests._load_module_safely backends.sqlite.tests_llm.CheckSQLiteVersionExtraTests._reload_module_with_version backends.sqlite.tests_llm.CheckSQLiteVersionExtraTests.test_function_allows_3_9_0 backends.sqlite.tests_llm.CheckSQLiteVersionExtraTests.test_function_raises_for_3_8_3 backends.sqlite.tests_llm.CheckSQLiteVersionExtraTests.test_import_allows_3_9_0 backends.sqlite.tests_llm.CheckSQLiteVersionExtraTests.test_import_raises_for_3_8_2 backends.sqlite.tests_llm.CheckSQLiteVersionExtraTests.test_import_raises_for_3_8_3 backends.sqlite.tests_llm.CheckSQLiteVersionExtraTests.test_message_contains_actual_version_on_import backends.sqlite.tests_llm.CheckSQLiteVersionExtraTests.test_no_raise_for_much_newer_version backends.sqlite.tests_llm.CheckSQLiteVersionExtraTests.test_tuple_with_extra_components_at_or_above_threshold_allows_on_import backends.sqlite.tests_llm.CheckSQLiteVersionExtraTests.test_tuple_with_extra_components_below_threshold_raises_on_import
coverage json -o coverage.json
: '>>>>> End Test Output'
