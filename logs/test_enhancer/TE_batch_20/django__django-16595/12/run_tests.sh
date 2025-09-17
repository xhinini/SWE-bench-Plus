#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_optimizer_llm.test_alter_then_remove_keeps_remove migrations.test_optimizer_llm.test_alterfields_case_insensitive_fieldname_collapses migrations.test_optimizer_llm.test_alterfields_case_insensitive_modelname_collapses migrations.test_optimizer_llm.test_different_fields_do_not_collapse migrations.test_optimizer_llm.test_multiple_alterfields_on_same_field_optimizes_quickly migrations.test_optimizer_llm.test_nonconsecutive_alterfields_preserve_unrelated migrations.test_optimizer_llm.test_remove_then_alter_keeps_remove migrations.test_optimizer_llm.test_three_alterfields_with_default_change_collapsed migrations.test_optimizer_llm.test_three_consecutive_alterfields_collapsed
coverage json -o coverage.json
: '>>>>> End Test Output'
