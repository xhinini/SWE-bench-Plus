#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_optimizer_llm.test_alterfield_and_other_model_same_field_name migrations.test_optimizer_llm.test_alterfield_case_insensitive_field_name migrations.test_optimizer_llm.test_alterfield_case_insensitive_model_and_field migrations.test_optimizer_llm.test_alterfield_different_models_not_collapsed migrations.test_optimizer_llm.test_alterfield_followed_by_rename_with_db_column_none migrations.test_optimizer_llm.test_alterfield_followed_by_rename_with_db_column_not_none migrations.test_optimizer_llm.test_alterfield_only_sequence_optimizes migrations.test_optimizer_llm.test_double_alterfield_collapses migrations.test_optimizer_llm.test_triple_alterfield_collapses_to_last
coverage json -o coverage.json
: '>>>>> End Test Output'
