#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_optimizer_llm.test_alter_managers_for_different_model_does_not_merge migrations.test_optimizer_llm.test_create_addfield_then_alter_managers migrations.test_optimizer_llm.test_create_alter_managers_then_addfield migrations.test_optimizer_llm.test_create_alter_model_managers_merge_custom migrations.test_optimizer_llm.test_create_alter_options_and_alter_managers migrations.test_optimizer_llm.test_create_alter_order_with_respect_to_and_alter_managers migrations.test_optimizer_llm.test_create_alter_unique_and_alter_managers migrations.test_optimizer_llm.test_create_multiple_alter_model_managers_last_wins migrations.test_optimizer_llm.test_create_remove_field_and_alter_managers migrations.test_optimizer_llm.test_create_rename_field_and_alter_managers
coverage json -o coverage.json
: '>>>>> End Test Output'
