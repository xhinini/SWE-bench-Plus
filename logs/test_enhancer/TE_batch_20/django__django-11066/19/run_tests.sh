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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 contenttypes_tests.test_operations_llm.ContentTypeRenameExtraTests.test_create_contenttypes_creates_missing_contenttypes_and_prints contenttypes_tests.test_operations_llm.ContentTypeRenameExtraTests.test_rename_uses_schema_editor_db_direct_call_backward
coverage json -o coverage.json
: '>>>>> End Test Output'
