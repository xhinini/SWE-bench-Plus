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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 contenttypes_tests.test_operations_llm.DenyMigrateRouter.allow_migrate contenttypes_tests.test_operations_llm.OtherDBRouter.allow_migrate contenttypes_tests.test_operations_llm.OtherDBRouter.db_for_write contenttypes_tests.test_operations_llm._get_schema_editor contenttypes_tests.test_operations_llm.test_conflict_on_other_db_does_not_modify_default contenttypes_tests.test_operations_llm.test_get_contenttypes_and_models_respects_router contenttypes_tests.test_operations_llm.test_inject_rename_contenttypes_operations_inserts_operation contenttypes_tests.test_operations_llm.test_missing_content_type_rename_noop contenttypes_tests.test_operations_llm.test_rename_aborts_when_router_disallows_migration contenttypes_tests.test_operations_llm.test_rename_backward_updates_correct_database contenttypes_tests.test_operations_llm.test_rename_clears_cache_after_success contenttypes_tests.test_operations_llm.test_rename_conflict_rolls_back_on_integrity_error contenttypes_tests.test_operations_llm.test_rename_respects_schema_editor_alias_when_saving contenttypes_tests.test_operations_llm.test_rename_updates_correct_database
coverage json -o coverage.json
: '>>>>> End Test Output'
