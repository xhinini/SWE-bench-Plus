#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_optimizer_llm.test_create_add_field_then_alter_managers migrations.test_optimizer_llm.test_create_alter_managers_among_unrelated_ops migrations.test_optimizer_llm.test_create_alter_managers_and_alter_options migrations.test_optimizer_llm.test_create_alter_managers_case_insensitive migrations.test_optimizer_llm.test_create_alter_managers_for_different_model_no_opt migrations.test_optimizer_llm.test_create_alter_model_managers_simple_extra migrations.test_optimizer_llm.test_create_preserves_bases_and_options_when_altering_managers migrations.test_optimizer_llm.test_create_rename_field_then_alter_managers migrations.test_optimizer_llm.test_create_then_alter_managers_then_add_field migrations.test_optimizer_llm.test_multiple_alter_model_managers_sequence
coverage json -o coverage.json
: '>>>>> End Test Output'
