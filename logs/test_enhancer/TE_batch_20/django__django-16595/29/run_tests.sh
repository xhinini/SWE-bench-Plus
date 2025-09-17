#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_optimizer_llm.test_alter_alter_case_insensitive_model_and_field migrations.test_optimizer_llm.test_alter_alter_collapses_to_second migrations.test_optimizer_llm.test_alter_followed_by_rename_with_db_column_set_does_not_move_alter migrations.test_optimizer_llm.test_alter_followed_by_single_rename_moves_alter_to_new_name migrations.test_optimizer_llm.test_alter_on_different_fields_does_not_collapse migrations.test_optimizer_llm.test_alter_preserve_default_flag_respected_when_collapsing migrations.test_optimizer_llm.test_alter_then_remove_field_case_insensitive migrations.test_optimizer_llm.test_alter_then_rename_then_alter_results_in_rename_then_alter migrations.test_optimizer_llm.test_three_alter_field_chain_keeps_last
coverage json -o coverage.json
: '>>>>> End Test Output'
