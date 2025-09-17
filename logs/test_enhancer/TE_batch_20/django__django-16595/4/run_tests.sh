#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_optimizer_llm.test_regression_alter_alter_case_insensitive migrations.test_optimizer_llm.test_regression_alter_alter_chain_collapses_to_last migrations.test_optimizer_llm.test_regression_alter_alter_collapses_simple migrations.test_optimizer_llm.test_regression_alter_alter_different_field_no_collapse migrations.test_optimizer_llm.test_regression_alter_alter_with_default_changes_collapses migrations.test_optimizer_llm.test_regression_alter_and_rename_field_db_column_none migrations.test_optimizer_llm.test_regression_alter_and_rename_field_db_column_not_none migrations.test_optimizer_llm.test_regression_alterfields_only_subsequence_optimized migrations.test_optimizer_llm.test_regression_alterfields_unrelated_model_no_collapse
coverage json -o coverage.json
: '>>>>> End Test Output'
