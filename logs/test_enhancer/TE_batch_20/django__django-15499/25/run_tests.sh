#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_optimizer_llm.test_create_add_field_then_alter_managers migrations.test_optimizer_llm.test_create_alter_managers_and_rename_model migrations.test_optimizer_llm.test_create_alter_managers_then_add_field migrations.test_optimizer_llm.test_create_alter_managers_then_alter_field migrations.test_optimizer_llm.test_create_alter_managers_then_alter_index_together migrations.test_optimizer_llm.test_create_alter_managers_then_alter_order_with_respect_to migrations.test_optimizer_llm.test_create_alter_managers_then_alter_unique_together migrations.test_optimizer_llm.test_create_alter_managers_then_remove_field migrations.test_optimizer_llm.test_create_alter_managers_then_rename_field migrations.test_optimizer_llm.test_create_alter_managers_with_reordering_fk
coverage json -o coverage.json
: '>>>>> End Test Output'
