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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 contenttypes_tests.test_operations_llm.test_clear_cache_called_on_successful_rename contenttypes_tests.test_operations_llm.test_clear_cache_not_called_on_conflict contenttypes_tests.test_operations_llm.test_get_contenttypes_and_models_respects_allow_migrate_model contenttypes_tests.test_operations_llm.test_inject_rename_contenttypes_operations_inserts_after_rename_model contenttypes_tests.test_operations_llm.test_inject_rename_contenttypes_operations_skips_when_contenttype_unavailable contenttypes_tests.test_operations_llm.test_missing_content_type_rename_does_nothing contenttypes_tests.test_operations_llm.test_rename_backward_uses_schema_editor_db contenttypes_tests.test_operations_llm.test_rename_conflict_restores_old_value contenttypes_tests.test_operations_llm.test_rename_ignored_if_allow_migrate_model_false contenttypes_tests.test_operations_llm.test_rename_uses_schema_editor_db_despite_router
coverage json -o coverage.json
: '>>>>> End Test Output'
