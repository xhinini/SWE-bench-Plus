#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_optimizer_llm.test_create_alter_field_and_managers_merge migrations.test_optimizer_llm.test_create_alter_managers_then_delete_model migrations.test_optimizer_llm.test_create_alter_managers_with_non_default_app_label migrations.test_optimizer_llm.test_create_alter_model_options_then_managers migrations.test_optimizer_llm.test_create_rename_then_alter_managers_merges migrations.test_optimizer_llm.test_create_with_default_objects_manager_removed_after_merge migrations.test_optimizer_llm.test_create_with_field_ops_and_alter_managers migrations.test_optimizer_llm.test_merge_alter_managers_case_insensitive migrations.test_optimizer_llm.test_multiple_alter_managers_last_wins
coverage json -o coverage.json
: '>>>>> End Test Output'
