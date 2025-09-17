#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_optimizer_llm.test_addfield_then_multiple_alter migrations.test_optimizer_llm.test_alter_alter_case_insensitive_model_and_name migrations.test_optimizer_llm.test_alter_alter_only_sequence migrations.test_optimizer_llm.test_alter_alter_only_sequence_multiple migrations.test_optimizer_llm.test_alter_alter_only_sequence_with_app_label migrations.test_optimizer_llm.test_alterfield_then_removefield migrations.test_optimizer_llm.test_alterfield_then_rename_db_column_none migrations.test_optimizer_llm.test_alterfield_then_rename_db_column_not_none migrations.test_optimizer_llm.test_alterfields_different_models_not_collapsed migrations.test_optimizer_llm.test_alterfields_different_names_not_collapsed
coverage json -o coverage.json
: '>>>>> End Test Output'
