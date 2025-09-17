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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 contenttypes_tests.test_operations_llm.test_missing_content_type_does_nothing_with_router contenttypes_tests.test_operations_llm.test_missing_content_type_does_nothing_without_router contenttypes_tests.test_operations_llm.test_rename_direct_call_updates_target_db_only contenttypes_tests.test_operations_llm.test_rename_does_not_create_in_default_when_default_has_unrelated_entry contenttypes_tests.test_operations_llm.test_rename_multiple_models_updates_only_target_db contenttypes_tests.test_operations_llm.test_rename_using_rename_backward_updates_target_db_only contenttypes_tests.test_operations_llm.test_rename_using_rename_backward_with_router_updates_target_db_only contenttypes_tests.test_operations_llm.test_rename_using_rename_forward_updates_target_db_only contenttypes_tests.test_operations_llm.test_rename_using_rename_forward_with_router_updates_target_db_only contenttypes_tests.test_operations_llm.test_rename_with_write_router_updates_target_db_only
coverage json -o coverage.json
: '>>>>> End Test Output'
