#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_optimizer_llm.test_alter_managers_name_case_insensitive migrations.test_optimizer_llm.test_alter_managers_replaces_rather_than_appends migrations.test_optimizer_llm.test_create_addfield_alter_managers_then_delete_model_collapses migrations.test_optimizer_llm.test_create_addfield_alter_options_alter_managers migrations.test_optimizer_llm.test_create_addfield_then_alter_managers migrations.test_optimizer_llm.test_create_alter_managers_then_addfield migrations.test_optimizer_llm.test_create_alter_managers_then_delete_model_collapses migrations.test_optimizer_llm.test_create_alter_options_and_managers migrations.test_optimizer_llm.test_create_removefield_then_alter_managers migrations.test_optimizer_llm.test_create_renamefield_then_alter_managers
coverage json -o coverage.json
: '>>>>> End Test Output'
