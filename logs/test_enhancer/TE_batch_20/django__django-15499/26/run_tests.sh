#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_optimizer_llm.test_create_add_field_alter_managers migrations.test_optimizer_llm.test_create_alter_managers_then_add_field migrations.test_optimizer_llm.test_create_alter_managers_then_delete migrations.test_optimizer_llm.test_create_alter_managers_with_rename migrations.test_optimizer_llm.test_create_alter_model_managers_chain migrations.test_optimizer_llm.test_create_alter_options_and_managers migrations.test_optimizer_llm.test_create_with_managers_then_alter_remove migrations.test_optimizer_llm.test_create_with_proxy_true_and_alter_managers migrations.test_optimizer_llm.test_multiple_models_alter_managers
coverage json -o coverage.json
: '>>>>> End Test Output'
