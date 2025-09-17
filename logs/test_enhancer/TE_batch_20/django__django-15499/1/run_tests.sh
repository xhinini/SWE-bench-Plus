#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_optimizer_llm.test_create_alter_model_managers_and_delete_disappears migrations.test_optimizer_llm.test_create_alter_model_managers_case_and_serialization migrations.test_optimizer_llm.test_create_alter_model_managers_case_insensitive migrations.test_optimizer_llm.test_create_alter_model_managers_default_to_custom migrations.test_optimizer_llm.test_create_alter_model_managers_duplicate_names_raises migrations.test_optimizer_llm.test_create_alter_model_managers_preserves_options_and_bases migrations.test_optimizer_llm.test_create_alter_model_managers_then_rename_absorbed migrations.test_optimizer_llm.test_create_alter_model_managers_with_rename_chain migrations.test_optimizer_llm.test_multiple_alter_model_managers_collapses_to_last
coverage json -o coverage.json
: '>>>>> End Test Output'
