#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_optimizer_llm.test_create_alter_managers_default_equivalence migrations.test_optimizer_llm.test_create_alter_model_managers_case_insensitive migrations.test_optimizer_llm.test_create_alter_preserve_options migrations.test_optimizer_llm.test_create_then_alter_and_addfield migrations.test_optimizer_llm.test_create_then_alter_managers_empty_list migrations.test_optimizer_llm.test_create_then_alter_managers_other_model_not_merged migrations.test_optimizer_llm.test_create_then_two_alter_managers_last_wins migrations.test_optimizer_llm.test_create_with_default_managers_then_alter migrations.test_optimizer_llm.test_create_with_existing_managers_overwritten migrations.test_optimizer_llm.test_create_without_managers_then_alter_sets_managers
coverage json -o coverage.json
: '>>>>> End Test Output'
