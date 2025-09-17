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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 contenttypes_tests.test_operations_llm.ContentTypeOperationsTestsExtra.test_direct_rename_conflict_on_other_db contenttypes_tests.test_operations_llm.ContentTypeOperationsTestsExtra.test_direct_rename_on_default_db contenttypes_tests.test_operations_llm.ContentTypeOperationsTestsExtra.test_direct_rename_on_other_db contenttypes_tests.test_operations_llm.ContentTypeOperationsTestsExtra.test_forward_rename_conflict_on_other_db contenttypes_tests.test_operations_llm.ContentTypeOperationsTestsExtra.test_rename_backward_on_default_db contenttypes_tests.test_operations_llm.ContentTypeOperationsTestsExtra.test_rename_backward_on_other_db contenttypes_tests.test_operations_llm.ContentTypeOperationsTestsExtra.test_rename_forward_on_default_db contenttypes_tests.test_operations_llm.ContentTypeOperationsTestsExtra.test_rename_forward_on_other_db contenttypes_tests.test_operations_llm.ContentTypeOperationsTestsExtra.test_rename_ignored_when_contenttype_missing_other_db contenttypes_tests.test_operations_llm.ContentTypeOperationsTestsExtra.test_rename_ignored_when_router_disallows_other_db
coverage json -o coverage.json
: '>>>>> End Test Output'
