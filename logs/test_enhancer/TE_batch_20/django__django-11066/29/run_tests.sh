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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 contenttypes_tests.test_operations_llm.AllowOtherRouter.allow_migrate_model contenttypes_tests.test_operations_llm.DenyAllRouter.allow_migrate_model contenttypes_tests.test_operations_llm.RenameContentTypeTests.setUp contenttypes_tests.test_operations_llm.RenameContentTypeTests.test_rename_saves_using_db contenttypes_tests.test_operations_llm.RenameContentTypeTests.test_router_denies_migration
coverage json -o coverage.json
: '>>>>> End Test Output'
