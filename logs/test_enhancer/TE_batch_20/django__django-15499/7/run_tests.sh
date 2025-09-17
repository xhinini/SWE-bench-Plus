#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_optimizer_llm.test_create_alter_managers_then_delete_model_collapses migrations.test_optimizer_llm.test_create_alter_model_managers_case_insensitive_name migrations.test_optimizer_llm.test_create_alter_model_managers_no_initial_managers migrations.test_optimizer_llm.test_create_alter_model_managers_preserve_fields migrations.test_optimizer_llm.test_create_alter_model_managers_preserve_options_and_bases migrations.test_optimizer_llm.test_create_alter_model_managers_simple_merge migrations.test_optimizer_llm.test_create_alter_model_managers_with_existing_managers_replaced migrations.test_optimizer_llm.test_create_rename_then_alter_model_managers migrations.test_optimizer_llm.test_multiple_alter_model_managers_chain
coverage json -o coverage.json
: '>>>>> End Test Output'
